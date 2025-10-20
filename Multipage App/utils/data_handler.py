import pandas as pd
from pathlib import Path
from datetime import datetime
import os

class DataHandler:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.participantes_file = self.data_dir / "participantes.csv"
        self.asistencias_file = self.data_dir / "asistencias.csv"
        self.equipos_file = self.data_dir / "equipos_concurso.csv"
        self.encuestas_file = self.data_dir / "encuesta_respuestas.csv"
        
        self.load_data()
    
    def load_data(self):
        """Carga todos los archivos CSV"""
        try:
            self.participantes = pd.read_csv(self.participantes_file)
            self.asistencias = pd.read_csv(self.asistencias_file)
            self.equipos = pd.read_csv(self.equipos_file)
            
            # Verificar si existe columna encuesta_completada
            if 'encuesta_completada' not in self.participantes.columns:
                self.participantes['encuesta_completada'] = 0
                self.save_participantes()
            
            # Cargar o crear archivo de encuestas
            if self.encuestas_file.exists():
                self.encuestas = pd.read_csv(self.encuestas_file)
            else:
                self.encuestas = pd.DataFrame(columns=[
                    'id', 'pregunta_id', 'participante_id', 'respuesta', 
                    'creado', 'actualizado'
                ])
                self.save_encuestas()
        except Exception as e:
            raise Exception(f"Error al cargar datos: {str(e)}")
    
    def save_participantes(self):
        """Guarda el DataFrame de participantes"""
        self.participantes.to_csv(self.participantes_file, index=False)
    
    def save_encuestas(self):
        """Guarda el DataFrame de encuestas"""
        self.encuestas.to_csv(self.encuestas_file, index=False)
    
    def get_participante_by_email(self, email):
        """Obtiene un participante por su correo electrónico"""
        result = self.participantes[self.participantes['correo'].str.lower() == email.lower()]
        if len(result) > 0:
            return result.iloc[0]
        return None
    
    def count_asistencias(self, participante_id):
        """Cuenta las asistencias de un participante"""
        return len(self.asistencias[self.asistencias['participante_id'] == participante_id])
    
    def get_workshop_participacion(self, participante_id):
        """Verifica si el participante asistió a un workshop"""
        asistencias = self.asistencias[self.asistencias['participante_id'] == participante_id]
        workshops = asistencias[asistencias['tipo_actividad'] == 'Workshop']
        
        if len(workshops) > 0:
            return True, workshops.iloc[0]['actividad_nombre']
        return False, None
    
    def get_mundialito_participacion(self, participante_id):
        """Verifica si el participante participó en el mundialito"""
        equipos = self.equipos[
            (self.equipos['integrante_1_id'] == participante_id) |
            (self.equipos['integrante_2_id'] == participante_id) |
            (self.equipos['integrante_3_id'] == participante_id) |
            (self.equipos['integrante_4_id'] == participante_id)
        ]
        
        return len(equipos) > 0
    
    def check_eligibility(self, email):
        """Verifica la elegibilidad de un participante para constancias"""
        participante = self.get_participante_by_email(email)
        
        if participante is None:
            return {
                'found': False,
                'message': 'Correo electrónico no encontrado en el sistema.'
            }
        
        participante_id = participante['id']
        asistencias_count = self.count_asistencias(participante_id)
        workshop_attended, workshop_name = self.get_workshop_participacion(participante_id)
        mundialito_attended = self.get_mundialito_participacion(participante_id)
        
        constancias_disponibles = []
        
        # Constancia de participación general
        if asistencias_count >= 2:
            constancias_disponibles.append({
                'tipo': 'participacion_general',
                'nombre': 'Constancia de Participación General',
                'plantilla': 'Participacion_general.pdf'
            })
        
        # Constancia de workshop
        if workshop_attended:
            # Extraer número de workshop del nombre
            workshop_num = self.extract_workshop_number(workshop_name)
            constancias_disponibles.append({
                'tipo': 'workshop',
                'nombre': f'Constancia de Workshop: {workshop_name}',
                'plantilla': f'W{workshop_num}.pdf',
                'workshop_nombre': workshop_name
            })
        
        # Constancia de mundialito
        if mundialito_attended:
            constancias_disponibles.append({
                'tipo': 'mundialito',
                'nombre': 'Constancia de Mundialito Mexicano',
                'plantilla': 'Constancia_mundialito.pdf'
            })
        
        return {
            'found': True,
            'participante': participante,
            'asistencias': asistencias_count,
            'workshop_attended': workshop_attended,
            'workshop_name': workshop_name if workshop_attended else None,
            'mundialito_attended': mundialito_attended,
            'constancias_disponibles': constancias_disponibles,
            'encuesta_completada': bool(participante['encuesta_completada'])
        }
    
    def extract_workshop_number(self, workshop_name):
        """Extrae el número del workshop del nombre"""
        import re
        match = re.search(r'[Ww]orkshop\s*(\d+)', workshop_name)
        if match:
            return match.group(1)
        return '1'
    
    def has_completed_survey(self, participante_id):
        """Verifica si el participante ya completó la encuesta"""
        return len(self.encuestas[self.encuestas['participante_id'] == participante_id]) > 0
    
    def save_survey_responses(self, participante_id, respuestas):
        """Guarda las respuestas de la encuesta"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Obtener el último ID
        if len(self.encuestas) > 0:
            last_id = self.encuestas['id'].max()
        else:
            last_id = 0
        
        nuevas_respuestas = []
        for pregunta_id, respuesta in respuestas.items():
            last_id += 1
            nuevas_respuestas.append({
                'id': last_id,
                'pregunta_id': pregunta_id,
                'participante_id': participante_id,
                'respuesta': str(respuesta),
                'creado': timestamp,
                'actualizado': timestamp
            })
        
        # Agregar nuevas respuestas
        new_df = pd.DataFrame(nuevas_respuestas)
        self.encuestas = pd.concat([self.encuestas, new_df], ignore_index=True)
        self.save_encuestas()
        
        # Actualizar flag en participantes
        self.participantes.loc[self.participantes['id'] == participante_id, 'encuesta_completada'] = 1
        self.save_participantes()
        
        return True
    
    def get_preguntas_encuesta(self):
        """Retorna las preguntas de la encuesta según el contexto"""
        preguntas = {
            'general': [
                {'id': 1, 'texto': '¿Cómo calificas la organización de la JII?', 'tipo': 'calificacion_1_5'},
                {'id': 2, 'texto': '¿Cómo calificas los horarios de la JII?', 'tipo': 'calificacion_1_5'},
                {'id': 3, 'texto': '¿Cómo calificas la duración de las actividades?', 'tipo': 'calificacion_1_5'},
                {'id': 4, 'texto': 'Especifica la razón principal por la que asististe a la JII:', 'tipo': 'texto_corto'},
                {'id': 5, 'texto': '¿Cumplieron tus expectativas las actividades en las que participaste?', 'tipo': 'calificacion_1_5'},
                {'id': 6, 'texto': '¿Los contenidos desarrollados resultaron útiles?', 'tipo': 'calificacion_1_5'},
                {'id': 7, 'texto': '¿Qué tan relevante consideras que fue el nivel profesional de la JII?', 'tipo': 'calificacion_1_5'},
                {'id': 8, 'texto': '¿Qué conferencia magistral te pareció la más relevante?', 'tipo': 'texto_corto'},
                {'id': 10, 'texto': '¿Qué actividad consideras que fue la de mayor relevancia?', 'tipo': 'texto_corto'},
                {'id': 11, 'texto': '¿Cuáles fueron para ti los puntos fuertes de la JII? ¿Por qué?', 'tipo': 'texto_largo'},
                {'id': 12, 'texto': '¿Qué parte te gustó menos? ¿Por qué?', 'tipo': 'texto_largo'},
                {'id': 13, 'texto': 'Propón tres temas de tu interés para la edición 2026 de la JII.', 'tipo': 'texto_largo'},
                {'id': 14, 'texto': '¿Qué sugerencias podrías aportar para mejorar la próxima edición de la JII?', 'tipo': 'texto_largo'},
                {'id': 15, 'texto': 'En términos generales, ¿Cómo calificaría la Jornada de Ingeniería Industrial 2025?', 'tipo': 'calificacion_1_5'},
                {'id': 16, 'texto': 'Comentarios adicionales:', 'tipo': 'texto_largo'}
            ],
            'workshop': [
                {'id': 17, 'texto': 'Valora el workshop al que asististe (1=Muy Malo, 5=Excelente)', 'tipo': 'calificacion_1_5'},
                {'id': 18, 'texto': 'Comentarios sobre el workshop', 'tipo': 'texto_largo'}
            ],
            'mundialito': [
                {'id': 19, 'texto': 'Valora el Mundialito Mexicano', 'tipo': 'calificacion_1_5'},
                {'id': 20, 'texto': 'Comentarios sobre el Mundialito Mexicano', 'tipo': 'texto_largo'}
            ]
        }
        
        return preguntas