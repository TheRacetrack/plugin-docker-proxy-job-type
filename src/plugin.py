class Plugin:
    def job_types(self) -> dict[str, dict]:
        """
        Job types provided by this plugin
        """
        plugin_version: str = getattr(self, 'plugin_manifest').version
        return {
            f'docker-proxy:{plugin_version}': {
                'images': [
                    {
                        'source': 'jobtype',
                        'dockerfile_path': 'job-template.Dockerfile',
                        'template': True,
                    },
                    {
                        'source': 'job',
                        'dockerfile_path': 'Dockerfile',
                        'template': False,
                    },
                ],
            },
        }
