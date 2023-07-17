import bpy
from ..operators.transformassist import GrabAssistOperator

class OverrideOperator(bpy.types.Operator):
    bl_idname = "mmz.override_operator"
    bl_label = "Shortcuts Override Operator"
    bl_options = {"REGISTER", "UNDO"}

    def grab_register(self, context):
        if bpy.context.scene.grab_pro.enabled:
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.addon
            if kc:
                km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
                kmi = km.keymap_items.new("mmz.grabassist_operator", "G", "PRESS")
                addon_keymaps.append((km, kmi))
        else:
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.addon
            if kc:
                for km, kmi in addon_keymaps:
                    if kmi.idname == "mmz.grabassist_operator":
                        km.keymap_items.remove(kmi)
                addon_keymaps.clear()
    
    def rotate_register(self, context):
        if bpy.context.scene.rotate_pro.enabled:
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.addon
            if kc:
                km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
                kmi = km.keymap_items.new("mmz.rotateassist_operator", "R", "PRESS")
                addon_keymaps.append((km, kmi))
        else:
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.addon
            if kc:
                for km, kmi in addon_keymaps:
                    if kmi.idname == "mmz.rotateassist_operator":
                        km.keymap_items.remove(kmi)
                addon_keymaps.clear()

    def resize_register(self, context):
        if bpy.context.scene.resize_pro.enabled:
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.addon
            if kc:
                km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
                kmi = km.keymap_items.new("mmz.resizeassist_operator", "S", "PRESS")
                addon_keymaps.append((km, kmi))
        else:
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.addon
            if kc:
                for km, kmi in addon_keymaps:
                    if kmi.idname == "mmz.resizeassist_operator":
                        km.keymap_items.remove(kmi)
                addon_keymaps.clear()

def register():
    global addon_keymaps
    addon_keymaps = []
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("mmz.addonmenu_piemenu_call", "X", "PRESS", alt=True)
        addon_keymaps.append((km, kmi))
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("mmz.switchlanguage_operator", "F1", "PRESS")
        addon_keymaps.append((km, kmi))


def unregister():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()

if __name__ == "__main__":
    register()
