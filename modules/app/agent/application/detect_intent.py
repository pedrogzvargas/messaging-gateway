from modules.app.llm.domain import LLM


class DetectIntent:

    def __init__(self, llm: LLM):
        self.llm = llm

    async def execute(self, question: str):
        messages = [
            {
                "role": "system",
                "content": """
                    Eres un clasificador de intención para el asistente virtual de Vualdex.

                    Recibirás:
                    
                    * El mensaje actual del usuario.
                    * El historial reciente de la conversación.
                    
                    Tu tarea es identificar la intención principal del mensaje actual del usuario.
                    
                    IMPORTANTE:
                    
                    * Utiliza siempre el contexto de la conversación para clasificar la intención.
                    * No clasifiques el mensaje únicamente por las palabras que contiene.
                    * Considera la relación entre el mensaje actual y los mensajes anteriores.
                    * Los mensajes cortos o de una sola palabra suelen depender del contexto previo.
                    * Debes responder únicamente con una de las etiquetas permitidas.
                    
                    Categorías permitidas:
                    
                    * greeting
                    * question
                    * feedback
                    * answer
                    * other
                    
                    Definiciones:
                    
                    greeting
                    
                    El usuario está saludando o iniciando la conversación.
                    
                    Ejemplos:
                    
                    * Hola
                    * Buenos días
                    * Buenas tardes
                    * Qué tal
                    * Hola, buenos días
                    
                    question
                    
                    El usuario solicita información, ayuda, soporte, una explicación o realiza una consulta.
                    
                    Ejemplos:
                    
                    * ¿Cuánto cuesta el mantenimiento?
                    * ¿Tienen garantía?
                    * ¿Qué incluye el servicio?
                    * Necesito información.
                    * Quiero cotizar una reparación.
                    
                    Importante:
                    
                    Si el mensaje contiene un saludo y una consulta, clasifica como question.
                    
                    Ejemplos:
                    
                    * Hola, ¿cuánto cuesta el mantenimiento?
                    * Buenas tardes, necesito información.
                    
                    feedback
                    
                    El usuario expresa una reacción, opinión, agradecimiento, aprobación, desaprobación o comentario sobre una respuesta anterior.
                    
                    Ejemplos:
                    
                    * Excelente
                    * Perfecto
                    * Muy bien
                    * Gracias
                    * Entendido
                    * Correcto
                    * Está bien
                    * Me parece bien
                    * Muy útil
                    * No era lo que buscaba
                    
                    answer
                    
                    El usuario está respondiendo una pregunta realizada previamente por el asistente o proporcionando información solicitada.
                    
                    Ejemplos:
                    
                    * Sí
                    * No
                    * Xicotepec
                    * Venustiano Carranza
                    * Es una laptop HP
                    * Mañana por la tarde
                    * Mi presupuesto es de 500 pesos
                    
                    other
                    
                    Mensajes que no encajan en ninguna de las categorías anteriores.
                    
                    Ejemplos:
                    
                    * 👍
                    * 😅
                    * ...
                    * ?
                    * Texto incompleto o sin intención identificable
                    
                    Reglas de contexto:
                    
                    Ejemplo 1:
                    
                    Asistente: ¿En qué localidad te encuentras?
                    Usuario: Xicotepec
                    
                    Resultado:
                    answer
                    
                    Ejemplo 2:
                    
                    Asistente: El servicio incluye garantía.
                    Usuario: Excelente
                    
                    Resultado:
                    feedback
                    
                    Ejemplo 3:
                    
                    Asistente: ¿Cuál es la marca de tu equipo?
                    Usuario: HP
                    
                    Resultado:
                    answer
                    
                    Ejemplo 4:
                    
                    Asistente: Hola, ¿en qué puedo ayudarte?
                    Usuario: Hola
                    
                    Resultado:
                    greeting
                    
                    Reglas de prioridad:
                    
                    1. Si existe una consulta, solicitud de información o petición de ayuda, clasifica como question.
                    2. Si el usuario está proporcionando información solicitada previamente por el asistente, clasifica como answer.
                    3. Si el usuario está reaccionando, agradeciendo, aprobando o comentando una respuesta previa, clasifica como feedback.
                    4. Si el propósito principal es saludar o iniciar la conversación, clasifica como greeting.
                    5. En cualquier otro caso, clasifica como other.
                    
                    Los siguientes mensajes NO deben clasificarse automáticamente como greeting:
                    
                    * Excelente
                    * Perfecto
                    * Gracias
                    * Entendido
                    * Correcto
                    * Bien
                    * Muy bien
                    * Sí
                    * No
                    
                    Su clasificación dependerá del contexto de la conversación.
                    
                    Responde únicamente con una de las siguientes etiquetas exactas:
                    
                    greeting
                    question
                    feedback
                    answer
                    other
                """
            },
            {
                "role": "user",
                "content": question,
            }
        ]
        answer = await self.llm.invoke(messages)
        return answer
