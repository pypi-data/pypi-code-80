from datetime import datetime
import os
import unittest
import datetime

import numpy as np
from pynwb import NWBFile, NWBHDF5IO, load_namespaces, get_class
from pynwb.ophys import TwoPhotonSeries, OpticalChannel, ImageSegmentation, PlaneSegmentation
from pynwb.testing import TestCase, remove_test_file, AcquisitionH5IOMixin

os.chdir('C:/Users/meowm/OneDrive/ProfessionalCode/NWBMeshAttributes/ndx-tan-lab-mesh-attributes/spec')
load_namespaces('ndx-tan-lab-mesh-attributes.namespace.yaml')
#Important to import Mesh Attributes first - N00b trip point
MeshAttributes = get_class('MeshAttributes', 'ndx-tan-lab-mesh-attributes')
MeshPlaneSegmentation = get_class('MeshPlaneSegmentation', 'ndx-tan-lab-mesh-attributes')

#1 - Create out of box NWB file with dummy data:

def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    device = nwbfile.create_device(
        name='device_name'
    )

    optical_channel_name = 'name'
    optical_channel_description = 'description'
    emission_lambda = 1.2
    excitation_lambda = 1.2
    grid_spacing_unit = 'um'
    
    #Create optical channel
    optical_channel = OpticalChannel(
        optical_channel_name,
        optical_channel_description,
        emission_lambda)

    #Create imaging plane
    imaging_plane = nwbfile.create_imaging_plane(
        'plane_name', 
        optical_channel, 
        'plane_description', 
        device, 
        excitation_lambda, 
        'indicator', 
        'location', 
        1.2, 
        grid_spacing= [1,1,1], 
        grid_spacing_unit = grid_spacing_unit)

    raw_data = TwoPhotonSeries(
        'Raw Data',
        format = 'external',
        rate = 1.2, 
        external_file = ['raw_data_link'],
        imaging_plane = imaging_plane,
        starting_frame = [1])

    nwbfile.add_acquisition(raw_data)

    return nwbfile

# #2 Add mesh attributes to constructor and confirm that they haven't changed 
class MeshAttributesConstructor(TestCase):
    def test_constructor(self):
        my_file = set_up_nwbfile()
        vertices = np.random.randn(20, 3)
        faces = np.random.randint(0, 20, (10, 3)).astype('uint')
        center_of_mass = [0,0,0]
        surface_area = 1.2
        volume = 1.2
        name = 'name'

        mesh_attributes = MeshAttributes(
            vertices=vertices,
            volume = volume,
            faces = faces,
            center_of_mass = center_of_mass,
            surface_area = surface_area,
            name = name)

        #Create OOB image segmentation
        segmentation_name = 'mesh_plane_segmentaton'
        raw_data = my_file.acquisition['Raw Data']
        imaging_plane = raw_data.imaging_plane
        module = my_file.create_processing_module('module for meshes', 'contains mesh data')        
        image_segmentation = ImageSegmentation()
        module.add(image_segmentation)
            
        #Create mesh plane segmentation from NWB extension    
        mesh_plane_segmentation = MeshPlaneSegmentation('output from segmenting a mesh',
                                imaging_plane, mesh_attributes, segmentation_name, raw_data)

        segmentation_name = 'mesh_plane_segmentaton'
        raw_data = my_file.acquisition['Raw Data']
        imaging_plane = raw_data.imaging_plane
            
        #Create plane segmentation from NWB extension    
        mesh_plane_segmentation = MeshPlaneSegmentation('output from segmenting a mesh',
                                imaging_plane, mesh_attributes, segmentation_name, raw_data)
 
        image_segmentation.add_plane_segmentation(mesh_plane_segmentation)

        #Test to see if values passed into mesh_attributes are the same:
        np.testing.assert_array_equal(mesh_attributes.vertices, vertices)
        self.assertEqual(mesh_attributes.volume, volume)
        np.testing.assert_array_equal(mesh_attributes.faces, faces)
        self.assertEqual(mesh_attributes.center_of_mass, center_of_mass)
        self.assertEqual(mesh_attributes.surface_area, surface_area)
        self.assertEqual(mesh_attributes.name, name)

        #Test to see if the processing modules containers are equal
        self.assertContainerEqual(module, my_file.processing['module for meshes'])
        #Test to see if plane_segmentation containers are equal
        mod = my_file.processing['module for meshes']
        self.assertContainerEqual(mesh_plane_segmentation, mod['ImageSegmentation'].get_plane_segmentation())

        print(mesh_plane_segmentation)
        print(mod['ImageSegmentation'].get_plane_segmentation())


        #4 Add Mesh Plane Segmentation to NWB file and confirm they haven't changed.
        with NWBHDF5IO('test.nwb', 'w') as io:
            io.write(my_file)

        with NWBHDF5IO('test.nwb', 'r') as io:
            nwbfile = io.read()
            self.assertContainerEqual(module, nwbfile.processing['module for meshes'])
            self.assertContainerEqual(mesh_plane_segmentation, mod['ImageSegmentation'].get_plane_segmentation())
        os.remove('test.nwb')

validation = MeshAttributesConstructor()
validation.test_constructor()
