from apache_beam.options.pipeline_options import PipelineOptions

class Config_Options(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--file_path',
            required=False,
            type=str
        )