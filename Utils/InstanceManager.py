class InstanceManager:

    instances = {}

    @staticmethod
    def add_instance(instance_name, instance):
        if instance_name in InstanceManager.instances:
            raise Exception("instance already exists")
        InstanceManager.instances[instance_name] = instance

    @staticmethod
    def get_instance(instance_name):
        return InstanceManager.instances[instance_name]
