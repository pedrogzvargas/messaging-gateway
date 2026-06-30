from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END
from .state import ChatState
from .nodes import DetectIntentNode, FeedbackNode, AnswerNode, OtherNode
from .nodes import GreetNode
from .nodes import FAQNode
from modules.app.agent.application import FAQ
from modules.app.agent.application import DetectIntent
from modules.app.agent.application import Feedback
from modules.app.agent.application import Answer
from modules.app.agent.application import Other
from modules.app.llm.domain import LLM
from modules.app.faq.domain import FaqRepository
from modules.app.message.domain import MessageRepository


class BusinessGraph:
    """
    Business Graph
    """
    def __init__(
        self,
        message_repository: MessageRepository,
        faq_repository: FaqRepository,
        llm: LLM,
    ):
        self.__message_repository = message_repository
        self.__faq_repository = faq_repository
        self.__llm = llm

    def build_graph(self):
        # services
        detect_intent = DetectIntent(llm=self.__llm)
        faq = FAQ(
            llm=self.__llm,
            faq_repository=self.__faq_repository,
            message_repository=self.__message_repository,
        )
        feedback = Feedback(llm=self.__llm, message_repository=self.__message_repository)
        answer = Answer(llm=self.__llm, message_repository=self.__message_repository)
        other = Other(llm=self.__llm, message_repository=self.__message_repository)
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
