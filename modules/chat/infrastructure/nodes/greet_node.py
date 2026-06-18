class GreetNode:

    def __call__(self, state):
        welcome_message = (
            "👋 *¡Bienvenido a Vualdex!*\n\n"
            "Somos una empresa enfocada en brindar soluciones tecnológicas que ayudan a optimizar y proteger tu negocio. 🚀\n\n"
            "*Nuestros servicios:*\n\n"
            "🔹 Desarrollo de software\n"
            "🔹 Instalación de cámaras de seguridad\n"
            "🔹 Licenciamiento de software\n"
            "🔹 Mantenimiento de equipos de cómputo\n\n"
            "🤖 Durante esta conversación estarás interactuando con nuestro asistente virtual, quien podrá ayudarte con información sobre nuestros servicios, cotizaciones y preguntas frecuentes.\n\n"
            "👨‍💼 Si necesitas atención personalizada, podremos canalizarte con uno de nuestros asesores.\n\n"
            "💬 *¿En qué podemos ayudarte hoy?*"
        )
        return {
            "response": welcome_message
        }
