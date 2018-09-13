class InstanceManager:

    instances = {}

    @staticmethod
    def add_instance(instance_name, instance):
        """
        Save an instance
        :param instance_name: Name of the instance, which will be needed to get this instance later
        :param instance: The instance of the object
        """
        if instance_name in InstanceManager.instances:
            raise Exception("instance already exists")
        InstanceManager.instances[instance_name] = instance

    @staticmethod
    def get_instance(instance_name):
        """
        Get a saved instance
        :param instance_name: The name of the instance as passed, when saving the instance
        :return: The instance
        """
        return InstanceManager.instances[instance_name]
