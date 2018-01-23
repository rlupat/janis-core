from pipeline_definition.types.step_type import StepFactory

class TrimFactory(StepFactory):
    @classmethod
    def describe(cls):
        return {
            'schema': {
                'trimmer': {
                    'type': 'string',
                    'allowed': ['cutadapt', 'trimmomatic'],
                    'default': 'trimmomatic'
                }
            },
            'nullable': True
        }

    @classmethod
    def build(cls, yml):
        return None

    @classmethod
    def type(cls):
        return 'trim'

    @classmethod
    def label(cls):
        return 'Trimmer'

    @classmethod
    def description(cls):
        return cls.label()

    @classmethod
    def emit(cls):
        return "Translation by " + cls.__name__
