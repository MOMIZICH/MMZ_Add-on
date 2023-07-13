import bpy
import datetime

bl_info = {
    "name": "MMZ Add-on",
    "author": "MOMIZI",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Tools > MMZ Add-on",
    "description": "機能詰め合わせ",
    "category": "General",
}

load_time = datetime.datetime.now()
load_time = str(load_time.replace(microsecond=2))
load_time = load_time.replace("-", ".")
load_time = load_time.replace(" ", "_")

print(f"MMZ Add-on: Info: loaded at {load_time}.")

if "bpy" in locals():
    import importlib
    for module_name in ["properties", "fanc_panels", "shortcuts", "transformassist"]:
        if module_name.title() in locals():
            importlib.reload(locals()[module_name.title()])

#from .func_panels import AutomergePanel
#from .func_panels import ExtrudeCancelPanel
from .operators.transformassist import GrabAssistOperator
from .operators.transformassist import RotateAssistOperator
from .operators.textsender import TextSenderOperator
from .operators.textsender import GetPreviousTextOperator
#from .resolution import ChangeResolutionOperator
from .preferences.shortcuts import OverrideOperator
from .panels.piemenu import MMZ_MT_AddonMenu
from .panels.piemenu import AddonPieMenu_Call
#from .automerge import AutoMergeOperator
from .operators.textremesh import TextRemeshOperator
#from .extrudecancel import ExtrudeCancelOperator
from .panels import func_panels
from .preferences import properties
from .preferences import shortcuts
from .operators import tools

classes = [
    #AutomergePanel,
    #ExtrudeCancelPanel,
    TextRemeshOperator,
    GrabAssistOperator,
    RotateAssistOperator,
    TextSenderOperator,
    GetPreviousTextOperator,
    OverrideOperator,
    #ChangeResolutionOperator,
    MMZ_MT_AddonMenu,
    AddonPieMenu_Call,
    #AutoMergeOperator,
    #ExtrudeCancelOperator,

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    func_panels.register()
    properties.register()
    shortcuts.register()
    tools.register()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    func_panels.unregister()
    properties.unregister()
    shortcuts.unregister()

if __name__ == "__main__":
    register()
