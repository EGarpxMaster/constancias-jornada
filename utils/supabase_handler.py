"""
Handler para almacenamiento de respuestas en Supabase
Opción más simple que Turso y Google Sheets - todo en el navegador
"""

import streamlit as st
from datetime import datetime
import os

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class SupabaseHandler:
    """Maneja la conexión y operaciones con Supabase"""
    
    def __init__(self):
        """Inicializa la conexión a Supabase"""
        if not SUPABASE_AVAILABLE:
            raise ImportError("supabase no está instalado. Ejecuta: pip install supabase")
        
        # Obtener credenciales desde Streamlit secrets o variables de entorno
        try:
            # Primero intenta Streamlit secrets (producción)
            self.url = st.secrets.get("SUPABASE_URL")
            self.key = st.secrets.get("SUPABASE_KEY")
        except:
            # Luego intenta variables de entorno (desarrollo local)
            self.url = os.getenv("SUPABASE_URL")
            self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError(
                "Credenciales de Supabase no encontradas. "
                "Define SUPABASE_URL y SUPABASE_KEY en secrets o .env"
            )
        
        self.client: Client = None
    
    def connect(self):
        """Establece conexión con Supabase"""
        try:
            self.client = create_client(self.url, self.key)
            return True
        except Exception as e:
            raise Exception(f"Error al conectar con Supabase: {str(e)}")
    
    def guardar_respuestas(self, email, nombre_completo, respuestas, preguntas_dict):
        """
        Guarda las respuestas de la encuesta en Supabase
        
        Args:
            email (str): Email del participante
            nombre_completo (str): Nombre completo del participante
            respuestas (dict): Diccionario {pregunta_id: respuesta}
            preguntas_dict (dict): Diccionario {pregunta_id: texto_pregunta}
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            if not self.client:
                self.connect()
            
            # 1. Eliminar respuestas previas del mismo participante
            self.client.table('encuesta_respuestas')\
                .delete()\
                .eq('participante_email', email.lower())\
                .execute()
            
            # 2. Preparar timestamp
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamp = int(datetime.now().timestamp())
            
            # 3. Preparar datos para inserción
            datos_insertar = []
            for pregunta_id, respuesta in respuestas.items():
                pregunta_texto = preguntas_dict.get(pregunta_id, f"Pregunta {pregunta_id}")
                
                datos_insertar.append({
                    'participante_email': email.lower(),
                    'nombre_completo': nombre_completo,
                    'pregunta_id': pregunta_id,
                    'pregunta_texto': pregunta_texto,
                    'respuesta': str(respuesta),
                    'fecha': fecha,
                    'timestamp': timestamp
                })
            
            # 4. Insertar todas las respuestas de una vez
            result = self.client.table('encuesta_respuestas')\
                .insert(datos_insertar)\
                .execute()
            
            return True
            
        except Exception as e:
            raise Exception(f"Error al guardar en Supabase: {str(e)}")
    
    def obtener_respuestas(self, email=None):
        """
        Obtiene respuestas de la base de datos
        
        Args:
            email (str, optional): Email del participante. Si es None, obtiene todas.
        
        Returns:
            list: Lista de diccionarios con las respuestas
        """
        try:
            if not self.client:
                self.connect()
            
            if email:
                response = self.client.table('encuesta_respuestas')\
                    .select('*')\
                    .eq('participante_email', email.lower())\
                    .order('pregunta_id')\
                    .execute()
            else:
                response = self.client.table('encuesta_respuestas')\
                    .select('*')\
                    .order('timestamp', desc=True)\
                    .execute()
            
            return response.data
            
        except Exception as e:
            raise Exception(f"Error al obtener respuestas de Supabase: {str(e)}")
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas básicas de las respuestas
        
        Returns:
            dict: Diccionario con estadísticas
        """
        try:
            if not self.client:
                self.connect()
            
            # Total de respuestas
            total_response = self.client.table('encuesta_respuestas')\
                .select('id', count='exact')\
                .execute()
            total_respuestas = total_response.count if hasattr(total_response, 'count') else 0
            
            # Obtener todas las respuestas para contar participantes únicos
            all_response = self.client.table('encuesta_respuestas')\
                .select('participante_email')\
                .execute()
            
            emails_unicos = set()
            if all_response.data:
                emails_unicos = {r['participante_email'] for r in all_response.data}
            
            # Última respuesta
            ultima_response = self.client.table('encuesta_respuestas')\
                .select('fecha')\
                .order('timestamp', desc=True)\
                .limit(1)\
                .execute()
            
            ultima_respuesta = None
            if ultima_response.data and len(ultima_response.data) > 0:
                ultima_respuesta = ultima_response.data[0]['fecha']
            
            return {
                'total_respuestas': total_respuestas,
                'total_participantes': len(emails_unicos),
                'ultima_respuesta': ultima_respuesta
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener estadísticas: {str(e)}")
    
    def obtener_respuestas_por_pregunta(self, pregunta_id):
        """
        Obtiene todas las respuestas de una pregunta específica
        
        Args:
            pregunta_id (int): ID de la pregunta
        
        Returns:
            list: Lista con las respuestas
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('encuesta_respuestas')\
                .select('nombre_completo, respuesta, fecha')\
                .eq('pregunta_id', pregunta_id)\
                .order('timestamp', desc=True)\
                .execute()
            
            return response.data
            
        except Exception as e:
            raise Exception(f"Error al obtener respuestas por pregunta: {str(e)}")
    
    def verificar_encuesta_completada(self, email):
        """
        Verifica si un participante ya completó la encuesta
        
        Args:
            email (str): Email del participante
        
        Returns:
            bool: True si completó la encuesta, False si no
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('participantes')\
                .select('encuesta_completada')\
                .eq('email', email.lower())\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0].get('encuesta_completada', False)
            
            return False
            
        except Exception as e:
            raise Exception(f"Error al verificar encuesta: {str(e)}")
    
    def marcar_encuesta_completada(self, email):
        """
        Marca la encuesta como completada para un participante
        
        Args:
            email (str): Email del participante
        
        Returns:
            bool: True si se actualizó exitosamente
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('participantes')\
                .update({'encuesta_completada': True})\
                .eq('email', email.lower())\
                .execute()
            
            return True
            
        except Exception as e:
            raise Exception(f"Error al marcar encuesta completada: {str(e)}")
    
    def obtener_participante(self, email):
        """
        Obtiene los datos de un participante desde Supabase
        
        Args:
            email (str): Email del participante
        
        Returns:
            dict: Datos del participante o None si no existe
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('participantes')\
                .select('*')\
                .eq('email', email.lower())\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener participante: {str(e)}")
    
    def obtener_todos_participantes(self):
        """
        Obtiene todos los participantes desde Supabase usando la vista completa
        que incluye el cálculo automático de total_asistencias y asistencias_confirmadas
        
        Returns:
            list: Lista de diccionarios con los participantes y sus estadísticas de asistencia
        """
        try:
            if not self.client:
                self.connect()
            
            # Usar la vista que ya calcula total_asistencias automáticamente
            response = self.client.table('vista_participantes_completa')\
                .select('*')\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            # Si falla la vista, intentar con tabla participantes como fallback
            try:
                response = self.client.table('participantes')\
                    .select('*')\
                    .execute()
                return response.data if response.data else []
            except:
                raise Exception(f"Error al obtener participantes: {str(e)}")
    
    def obtener_todas_asistencias(self):
        """
        Obtiene todas las asistencias desde Supabase
        
        Returns:
            list: Lista de diccionarios con las asistencias
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('asistencias')\
                .select('*')\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error al obtener asistencias: {str(e)}")
    
    def obtener_todas_actividades(self):
        """
        Obtiene todas las actividades desde Supabase
        
        Returns:
            list: Lista de diccionarios con las actividades
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('actividades')\
                .select('*')\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error al obtener actividades: {str(e)}")
    
    def obtener_todos_equipos(self):
        """
        Obtiene todos los equipos del concurso desde Supabase
        
        Returns:
            list: Lista de diccionarios con los equipos
        """
        try:
            if not self.client:
                self.connect()
            
            response = self.client.table('equipos_concurso')\
                .select('*')\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error al obtener equipos: {str(e)}")


# Función de utilidad para uso rápido
def guardar_respuestas_supabase(email, nombre_completo, respuestas, preguntas_dict):
    """
    Función de utilidad para guardar respuestas rápidamente
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        handler = SupabaseHandler()
        handler.guardar_respuestas(email, nombre_completo, respuestas, preguntas_dict)
        return True, "Respuestas guardadas exitosamente en Supabase"
    except ImportError:
        return False, "supabase no instalado. Ejecuta: pip install supabase"
    except ValueError as e:
        return False, f"Configuración: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"
