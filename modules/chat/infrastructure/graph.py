from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END
from .state import ChatState
from .nodes import DetectIntentNode, FeedbackNode, AnswerNode, OtherNode
from .nodes import GreetNode
from .nodes import FAQNode
from modules.chat.application import FAQ
from modules.chat.application import DetectIntent
from modules.chat.application import Feedback
from modules.chat.application import Answer
from modules.chat.application import Other
from modules.chat.domain import LLM
from modules.chat.domain import QuestionRepository
from modules.whatsapp_message.domain import WhatsappMessageRepository


class AIGraph:
    """
    AI Graph
    """
    def __init__(
        self,
        whatsapp_message_repository: WhatsappMessageRepository,
        question_repository: QuestionRepository,
        llm: LLM,
    ):
        self.__whatsapp_message_repository = whatsapp_message_repository
        self.__question_repository = question_repository
        self.__llm = llm

    def build_graph(self):
        # services
        detect_intent = DetectIntent(llm=self.__llm)
        faq = FAQ(
            llm=self.__llm,
            question_repository=self.__question_repository,
            whatsapp_message_repository=self.__whatsapp_message_repository,
        )
        feedback = Feedback(llm=self.__llm, whatsapp_message_repository=self.__whatsapp_message_repository)
        answer = Answer(llm=self.__llm, whatsapp_message_repository=self.__whatsapp_message_repository)
        other = Other(llm=self.__llm, whatsapp_message_repository=self.__whatsapp_message_repository)
        # nodes
        detect_intent_node = DetectIntentNode(service=detect_intent)
        greet_node = GreetNode()
        faq_node = FAQNode(service=faq)
        feedback_node = FeedbackNode(service=feedback)
        answer_node = AnswerNode(service=answer)
        other_node = OtherNode(service=other)

        graph = StateGraph(ChatState)

        def route(state):
            return state.intent

        graph.add_node("detect_intent", detect_intent_node)
        graph.add_node("greet", greet_node)
        graph.add_node("faq", faq_node)
        graph.add_node("feedback", feedback_node)
        graph.add_node("answer", answer_node)
        graph.add_node("other", other_node)

        graph.add_edge(START, "detect_intent")
        graph.add_conditional_edges(
            "detect_intent",
            route,
            {
                "question": "faq",
                "greeting": "greet",
                "feedback": "feedback",
                "answer": "answer",
                "other": "other",
            }
        )

        graph.add_edge("greet", END)
        graph.add_edge("faq", END)
        graph.add_edge("feedback", END)
        graph.add_edge("answer", END)
        graph.add_edge("other", END)

        return graph.compile()
