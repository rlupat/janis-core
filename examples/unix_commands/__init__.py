from pipeline_definition.types.type_registry import register_tool, register_type
# , register_input_factory, register_step_factory

# from examples.unix_commands.data_types.class_file import ClassFileFactory
from examples.unix_commands.steps.compile import Compile
from examples.unix_commands.steps.untar import Untar
from examples.unix_commands.steps.tar import Tar

from examples.unix_commands.data_types.tar_file import TarFile #, TarFileFactory
# from examples.unix_commands.data_types.generic_file import GenericFileFactory
# from examples.unix_commands.data_types.string import StringFactory

# register_input_factory(TarFileFactory())
# register_input_factory(GenericFileFactory())
# register_input_factory(ClassFileFactory())
# register_input_factory(StringFactory())
#
# register_step_factory(CompileFactory())
# register_step_factory(UntarFactory())
# register_step_factory(TarFactory())

register_type(TarFile)

register_tool(Tar)
register_tool(Untar)
register_tool(Compile)

