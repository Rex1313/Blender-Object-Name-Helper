bl_info = {
    "name": "Name Utilities",
    "description": "Mesh and Object name helper",
    "author": "Sylwester Moniuszko-Szymanski",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Object Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "https://github.com/Rex1313/Blender-Object-Name-Helper",
    "category": "Mesh"
}


import bpy
import bmesh

from bpy.types import (Panel,
                       PropertyGroup,
                       Operator
                       )

# ------------------------------------------------------------------------
#    Dialog for Checking Names
# ------------------------------------------------------------------------


class NameCheckDialog(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.dialog_operator"
    bl_label = "Default Names Check"
    bl_options = {'REGISTER', 'UNDO'}
    
    def checkIsCustom(self, object_name):
        custom_names = ['Cube', 'Sphere', 'Plane','Cylinder','Cone','Torus','Icosphere','Circle','Path','Bezier','NurbsCurve','BezierCircle','NurbsPath','Text','Armature','Empty']
        if (len(list(filter (lambda name : name in object_name, custom_names))) > 0):
           return True
        return False   
    

    def draw(self, context):
        custom_object_names = []
        custom_mesh_names = []
        layout = self.layout
        for object in bpy.data.objects:
            if(self.checkIsCustom(object.name)):
                custom_object_names.insert(len(custom_object_names),object.name)
            if(self.checkIsCustom(object.data.name)):
                custom_mesh_names.insert(len(custom_mesh_names),object.name)
        if len(custom_object_names)==0 and len(custom_mesh_names)==0:
            layout.label(text='Congratulations!')
            layout.label(text='You do not have custom names in your project')
        if(len(custom_object_names))!=0:
            layout.label(text='You have '+ str(len(custom_object_names)) +' Object/s with default name:')
        for name in custom_object_names:
            print(name)
            layout.label(text=name)
        if(len(custom_mesh_names))!=0:
            layout.label(text='You have '+str(len(custom_mesh_names))+' Mesh/es with default name in Object/s:')
        for name in custom_mesh_names:
            layout.label(text=name)
        

    def execute(self, context):
        return {'FINISHED'} 

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_MatchMeshNames(Operator):
    bl_label = "Match mesh names"
    bl_idname = "wm.mesh_renamer"
    
    def execute(self, context):
        for obj in bpy.data.objects:
            obj.data.name=obj.name
            
        return {'FINISHED'}  

# ------------------------------------------------------------------------
#    Panel in Edit Mode
# ------------------------------------------------------------------------

class OBJECT_PT_ObjectToolPanel(Panel):
    bl_label = "Mesh Renamer"
    bl_idname = "OBJECT_PT_mesh_renamer"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Object Tools"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.operator("wm.mesh_renamer")
        layout.separator()
        layout.operator("object.dialog_operator")
        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    WM_OT_MatchMeshNames,
    OBJECT_PT_ObjectToolPanel,
    NameCheckDialog
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)