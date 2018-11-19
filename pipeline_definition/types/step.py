from abc import ABC, abstractmethod
from typing import List, Dict, Any

from pipeline_definition.graph.node import Node, NodeType
from pipeline_definition.types.tool import Tool, ToolInput, ToolOutput
from pipeline_definition.utils.logger import Logger


class Step:
    def __init__(self, label: str, tool: Tool, meta: Dict[str, Any]):
        self.__label: str = label
        self.__tool: Tool = tool
        self.__meta: Dict[str, Any] = meta

    def __str__(self):
        l = self.__label
        t = self.__tool
        return f"{l}: {t}"

    def id(self):
        return self.__label

    def input_value(self, tag) -> str:
        return self.__meta[tag]

    def requires(self) -> Dict[str, ToolInput]:
        return self.__tool.inputs_map()

    def provides(self) -> Dict[str, ToolOutput]:
        return self.__tool.outputs_map()

    @staticmethod
    def select_type_name_from(meta) -> str:
        return meta["tool"]


class StepNode(Node):
    def __init__(self, step: Step):
        super().__init__(NodeType.TASK, step.id())
        self.step = step

    def inputs(self) -> Dict[str, ToolInput]:
        return self.step.requires()

    def outputs(self) -> Dict[str, ToolOutput]:
        return self.step.provides()


# Should be able to remove the below


class StepFactory(ABC):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def label(cls) -> str:
        pass

    @classmethod
    def description(cls) -> str:
        return cls.label()

    @classmethod
    @abstractmethod
    def schema(cls) -> dict:
        pass

    @classmethod
    @abstractmethod
    def build(cls, label: str, meta: dict) -> Step:
        pass

    @classmethod
    def support_translations(cls) -> List[str]:
        return ['cwl']

    @classmethod
    def build_from(cls, label: str, step_meta: dict) -> Step:
        step_type = cls.type()
        Logger.log(f"{step_type} factory: Building from {step_meta}")
        obj = cls.build(label, step_meta)
        # obj.identify()
        return obj


class TaggedDatum(ABC):
    @abstractmethod
    def tags(self):
        # A set tags that can select among similar types
        pass

    @abstractmethod
    def datum_type(self):
        # A datum_type
        pass

    def satisfies(self, datum):
        # A concrete implementation here
        pass
