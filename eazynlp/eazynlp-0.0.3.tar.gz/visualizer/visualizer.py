class Visualization:
    """
    Superclass that defines the basic properties and methods
    supported by child classes that implement specific visualizations.
    """
    visualization = None

    def __init__(self):
        pass

    def show_visualization(self, visual_type):
        """
        Shell method for showing visualization in child class
        :param visual_type: Type of visualization
        """
        pass

    def save_visualization(self, visual_type, target_filepath=None):
        """
        Shell method for saving analysis result in child class
        to a file
        :param visual_type: Type of visualization
        :param target_filepath: Target filepath to save visualization
        """
        pass
