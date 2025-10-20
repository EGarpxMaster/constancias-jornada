from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import io

class PDFGenerator:
    def __init__(self, assets_dir):
        self.assets_dir = Path(assets_dir)
        self.fonts_dir = self.assets_dir / "fonts"
        self.plantillas_dir = self.assets_dir / "plantillas"
        
        # Registrar fuentes
        self.register_fonts()
    
    def register_fonts(self):
        """Registra las fuentes personalizadas"""
        try:
            pdfmetrics.registerFont(
                TTFont('OldStandard-Bold', str(self.fonts_dir / 'OldStandardTT-Bold.ttf'))
            )
            pdfmetrics.registerFont(
                TTFont('OldStandard-Regular', str(self.fonts_dir / 'OldStandardTT-Regular.ttf'))
            )
            pdfmetrics.registerFont(
                TTFont('OldStandard-Italic', str(self.fonts_dir / 'OldStandardTT-Italic.ttf'))
            )
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar las fuentes personalizadas: {e}")
    
    def generate_constancia(self, plantilla_nombre, nombre_completo, output_path=None):
        """
        Genera una constancia personalizada
        
        Args:
            plantilla_nombre: Nombre del archivo de plantilla (ej: 'Participacion_general.pdf')
            nombre_completo: Nombre completo del participante
            output_path: Ruta donde guardar el PDF (opcional)
        
        Returns:
            bytes del PDF generado
        """
        plantilla_path = self.plantillas_dir / plantilla_nombre
        
        if not plantilla_path.exists():
            raise FileNotFoundError(f"Plantilla no encontrada: {plantilla_path}")
        
        # Leer la plantilla
        reader = PdfReader(str(plantilla_path))
        writer = PdfWriter()
        
        # Crear un PDF temporal con el nombre
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Configurar el texto del nombre
        # Ajusta estas coordenadas según tu plantilla
        page_width, page_height = letter
        
        # Configuración para el nombre
        can.setFont('OldStandard-Bold', 24)
        can.setFillColorRGB(0, 0, 0)  # Negro
        
        # Calcular el centro de la página
        text_width = can.stringWidth(nombre_completo, 'OldStandard-Bold', 24)
        x_position = (page_width - text_width) / 2
        
        # Posición Y (ajusta según tu plantilla)
        # Esta es una posición aproximada, ajústala según tu diseño
        y_position = page_height / 2  # Centro vertical
        
        can.drawString(x_position, y_position, nombre_completo)
        can.save()
        
        # Mover al inicio del buffer
        packet.seek(0)
        
        # Leer el PDF temporal
        overlay = PdfReader(packet)
        
        # Combinar con la plantilla
        page = reader.pages[0]
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
        
        # Si hay más páginas en la plantilla, agregarlas
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])
        
        # Escribir el resultado
        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)
        
        # Si se especificó una ruta, guardar también ahí
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(output_stream.getvalue())
            output_stream.seek(0)
        
        return output_stream.getvalue()
    
    def generate_multiple_constancias(self, constancias_info, nombre_completo):
        """
        Genera múltiples constancias para un participante
        
        Args:
            constancias_info: Lista de diccionarios con info de constancias
            nombre_completo: Nombre completo del participante
        
        Returns:
            Dict con bytes de cada constancia generada
        """
        resultados = {}
        
        for constancia in constancias_info:
            try:
                pdf_bytes = self.generate_constancia(
                    constancia['plantilla'],
                    nombre_completo
                )
                resultados[constancia['tipo']] = {
                    'bytes': pdf_bytes,
                    'nombre': constancia['nombre'],
                    'filename': f"Constancia_{constancia['tipo']}_{nombre_completo.replace(' ', '_')}.pdf"
                }
            except Exception as e:
                print(f"Error generando constancia {constancia['tipo']}: {e}")
                resultados[constancia['tipo']] = None
        
        return resultados


class SimplePDFGenerator:
    """
    Generador simplificado que solo escribe sobre plantillas existentes
    sin necesidad de PyPDF2 si hay problemas
    """
    def __init__(self, assets_dir):
        self.assets_dir = Path(assets_dir)
        self.fonts_dir = self.assets_dir / "fonts"
        self.plantillas_dir = self.assets_dir / "plantillas"
        
        try:
            pdfmetrics.registerFont(
                TTFont('OldStandard-Bold', str(self.fonts_dir / 'OldStandardTT-Bold.ttf'))
            )
        except:
            pass
    
    def generate_simple_constancia(self, plantilla_nombre, nombre_completo):
        """
        Genera una constancia simple sin overlay
        """
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        page_width, page_height = letter
        
        # Título
        can.setFont('OldStandard-Bold', 28)
        can.drawCentredString(page_width / 2, page_height - 100, "CONSTANCIA")
        
        # Texto
        can.setFont('OldStandard-Regular', 14)
        text = f"Se otorga la presente constancia a:"
        can.drawCentredString(page_width / 2, page_height - 200, text)
        
        # Nombre
        can.setFont('OldStandard-Bold', 24)
        can.drawCentredString(page_width / 2, page_height / 2, nombre_completo)
        
        # Más texto
        can.setFont('OldStandard-Regular', 12)
        can.drawCentredString(page_width / 2, page_height / 2 - 100, 
                            "Por su participación en la Jornada de Ingeniería Industrial 2025")
        
        can.save()
        packet.seek(0)
        
        return packet.getvalue()