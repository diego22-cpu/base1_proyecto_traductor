from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QMessageBox, QApplication
import sys
import os  

class TraductorApp(QMainWindow):
    def __init__(self, ui_file):
        super().__init__()
        try:
            # Carga la interfaz gráfica
            uic.loadUi(ui_file, self)
        except Exception as e:
            print(f"Error crítico al cargar UI: {e}")
            print(f"Ruta intentada: {ui_file}")
            sys.exit(1)

        # --- DICCIONARIO (LÉXICO) ---
        self.tokens = {
            'a': "11", 'b': "12", 'c': "13", 'd': "14", 'e': "15", 'f': "16",
            'g': "17", 'h': "18", 'i': "19", 'j': "20", 'k': "21", 'l': "22",
            'm': "23", 'n': "24", 'o': "25", 'p': "26", 'q': "27", 'r': "28",
            's': "29", 't': "30", 'u': "31", 'v': "32", 'w': "33", 'x': "34",
            'y': "35", 'z': "36", 'espacio': ".",
            
            'LUNES': "2231241529", 'MARTES': "231128301529", 'MIERCOLES': "231915281325221529",
            'JUEVES': "203115321529", 'VIERNES': "32191528241529", 'SABADO': "291112111425",
            'DOMINGO': "14252319241725",
            
            'DIA': "141911", 'SEMANA': "291523112411"
        }
        self.reverse_tokens = {v: k for k, v in self.tokens.items()}
        
        # Estructuras de memoria
        self.tabla_simbolos = []
        self.codigo_intermedio = []
        self.codigo_optimizado = []

        # --- UI ELEMENTS ---
        self.text_entrada = self.findChild(QTextEdit, "text_entrada")
        self.text_salida = self.findChild(QTextEdit, "text_salida")
        self.btn_traducir = self.findChild(QPushButton, "btn_traducir")
        self.btn_limpiar = self.findChild(QPushButton, "btn_limpiar")
        self.btn_ayuda = self.findChild(QPushButton, "btn_ayuda")

        # Conectar botones del teclado virtual
        for button_name in self.tokens.keys():
            button = self.findChild(QPushButton, button_name)
            if button:
                button.clicked.connect(lambda _, name=button_name: self.on_button_click(name))

        # Conectar botones funcionales
        if self.btn_traducir: self.btn_traducir.clicked.connect(self.compilar_texto)
        if self.btn_limpiar: self.btn_limpiar.clicked.connect(self.limpiar_campos)
        if self.btn_ayuda: self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

    def on_button_click(self, button_name):
        if button_name in self.tokens:
            texto_insercion = self.tokens[button_name]
            self.text_entrada.insertPlainText("." if button_name == 'espacio' else texto_insercion)

    # --- UTILIDAD PARA IMPRIMIR EN CONSOLA ---
    def imprimir_encabezado(self, titulo):
        ancho = 60
        print("\n" + "╔" + "═" * (ancho - 2) + "╗")
        print(f"║ {titulo:^{ancho - 4}} ║")
        print("╚" + "═" * (ancho - 2) + "╝")

    def imprimir_separador(self):
        print("-" * 60)

    # ==========================================
    # FASE 1: ANÁLISIS LÉXICO
    # ==========================================
    def analizar_lexico(self, entrada):
        bloques = entrada.split(".")
        tokens_validos = []
        for bloque in bloques:
            if not bloque: continue 
            # Validación de longitud par
            if len(bloque) % 2 != 0:
                QMessageBox.warning(self, "Error Léxico", f"Longitud impar: '{bloque}'")
                return None
            
            # Validación de existencia en diccionario
            es_valido = bloque in self.reverse_tokens or \
                        all(bloque[i:i+2] in self.reverse_tokens for i in range(0, len(bloque), 2))
            
            if not es_valido:
                QMessageBox.warning(self, "Error Léxico", f"Código desconocido: '{bloque}'")
                return None
            tokens_validos.append(bloque)
        return tokens_validos

    # ==========================================
    # FASE 2: ANÁLISIS SINTÁCTICO
    # ==========================================
    def analizar_sintactico(self, entrada):
        if ".." in entrada:
            QMessageBox.warning(self, "Error Sintáctico", "Doble espacio (..) no permitido.")
            return False
        if entrada.startswith(".") or entrada.endswith("."):
            QMessageBox.warning(self, "Error Sintáctico", "Punto inicial o final no permitido.")
            return False
        return True

    # ==========================================
    # FASE 3: ANÁLISIS SEMÁNTICO (Unidad 1)
    # ==========================================
    def analizar_semantico(self, tokens):
        self.tabla_simbolos = []
        self.imprimir_encabezado("FASE 1: ANÁLISIS SEMÁNTICO (Tabla de Símbolos)")
        
        # Encabezado de la tabla
        print(f"| {'POS':<3} | {'TOKEN (LEXEMA)':<20} | {'TIPO':<10} | {'VALOR':<15} |")
        print("|" + "-"*5 + "|" + "-"*22 + "|" + "-"*12 + "|" + "-"*17 + "|")

        for i, token in enumerate(tokens):
            if len(token) == 2:
                tipo = "CHAR"
                valor = self.reverse_tokens.get(token, "?")
            else:
                tipo = "STRING"
                valor = self.reverse_tokens.get(token, "Compuesto")
            
            self.tabla_simbolos.append({"token": token, "tipo": tipo, "valor": valor})
            print(f"| {i+1:<3} | {token:<20} | {tipo:<10} | {valor:<15} |")
        self.imprimir_separador()
        return True

    # ==========================================
    # FASE 4: CÓDIGO INTERMEDIO (Unidad 2)
    # ==========================================
    def generar_codigo_intermedio(self):
        self.codigo_intermedio = []
        self.imprimir_encabezado("FASE 2: GENERACIÓN CÓDIGO INTERMEDIO")
        
        temp_counter = 1
        print(f"{'LINEA':<8} {'INSTRUCCIÓN'}")
        self.imprimir_separador()

        for item in self.tabla_simbolos:
            temporal = f"T{temp_counter}"
            instruccion = f"{temporal} = DECODE({item['token']})"
            self.codigo_intermedio.append(instruccion)
            print(f"{temp_counter:<8} {instruccion}")
            temp_counter += 1
        self.imprimir_separador()

    # ==========================================
    # FASE 5: OPTIMIZACIÓN (Unidad 4)
    # ==========================================
    def optimizar_codigo(self):
        self.codigo_optimizado = []
        self.imprimir_encabezado("FASE 3: OPTIMIZACIÓN (Código Redundante)")
        
        temporales_existentes = {} 
        temp_counter = 1
        linea_opt = 1

        print(f"{'LINEA':<8} {'ACCION':<15} {'DETALLE'}")
        self.imprimir_separador()

        for item in self.tabla_simbolos:
            token = item['token']
            
            if token in temporales_existentes:
                # Caso Optimizado: Reutilización
                temporal_viejo = temporales_existentes[token]
                accion = "[OPTIMIZADO]"
                detalle = f"REUSE {temporal_viejo} (Ya calculado)"
                print(f"{linea_opt:<8} {accion:<15} {detalle}")
            else:
                # Caso Normal: Nuevo cálculo
                temporal = f"T{temp_counter}"
                temporales_existentes[token] = temporal
                accion = "[NUEVO]"
                detalle = f"{temporal} = DECODE({token})"
                print(f"{linea_opt:<8} {accion:<15} {detalle}")
                temp_counter += 1
            linea_opt += 1
        self.imprimir_separador()

    # ==========================================
    # FASE 6: CÓDIGO FINAL (Unidad 3)
    # ==========================================
    def generar_codigo_final(self):
        salida_texto = ""
        for item in self.tabla_simbolos:
            token = item['token']
            if token in self.reverse_tokens:
                salida_texto += self.reverse_tokens[token] + " "
            else:
                palabra = ""
                for i in range(0, len(token), 2):
                    par = token[i:i+2]
                    palabra += self.reverse_tokens.get(par, "?")
                salida_texto += palabra + " "
        return salida_texto.strip()

    # --- FUNCIÓN PRINCIPAL DE EJECUCIÓN ---
    def compilar_texto(self):
        entrada = self.text_entrada.toPlainText().strip()
        if not entrada:
            QMessageBox.warning(self, "Advertencia", "Entrada vacía.")
            return

        print("\n\n" + "#"*60)
        print(f"{' INICIO DE COMPILACIÓN ':#^60}")
        print("#"*60)

        # Pipeline de compilación
        tokens = self.analizar_lexico(entrada)
        if tokens is None: return
        if not self.analizar_sintactico(entrada): return
        
        self.analizar_semantico(tokens)
        self.generar_codigo_intermedio()
        self.optimizar_codigo()
        
        resultado = self.generar_codigo_final()
        self.text_salida.setPlainText(resultado)
        
        self.imprimir_encabezado("RESULTADO FINAL")
        print(f" >> {resultado}")
        print("╚" + "═" * 58 + "╝\n")

    def limpiar_campos(self):
        self.text_entrada.clear()
        self.text_salida.clear()
        self.tabla_simbolos = []
        print("\n--- SISTEMA LIMPIO ---\n")

    def mostrar_ayuda(self):
        mensaje = (
            "📌 **GUÍA DE USUARIO **\n\n"
            "**1. Instrucciones Básicas:**\n"
            "• Escribe usando los botones de señas o el teclado.\n"
            "• Usa el botón 'Espacio' para separar palabras (se ve como un punto).\n"
            "• Presiona 'TRADUCIR' para ver el resultado.\n\n"
            
            "**2. funciones de consola :**\n"
            "• ¡Mira la CONSOLA NEGRA! Ahí verás:\n"
            "   - La Tabla de Símbolos (Análisis Semántico).\n"
            "   - Cómo se genera el Código Intermedio.\n"
            "   - La Optimización (si repites señas).\n\n"

            "**3. Solución de Errores Comunes:**\n"
            "❌ *Error Léxico:* Código impar (ej. '123') o desconocido.\n"
            "❌ *Error Sintáctico:* Dos puntos seguidos (..) o terminar en punto.\n"
        )
        QMessageBox.information(self, "Ayuda del Traductor", mensaje)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # --- FIX ROBUSTO PARA RUTA DE ARCHIVOS ---
    # Obtiene la carpeta donde está guardado este script .py
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Combina esa carpeta con el nombre del archivo UI
    ui_file = os.path.join(directorio_actual, "Traductor.ui")
    
    # Imprimimos la ruta para depuración (opcional)
    print(f"Buscando interfaz en: {ui_file}")
    
    ventana = TraductorApp(ui_file)
    ventana.show()
    sys.exit(app.exec_())