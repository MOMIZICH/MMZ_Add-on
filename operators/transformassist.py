import bpy

class GrabAssistOperator(bpy.types.Operator):
    bl_idname = "mmz.grabassist_operator"
    bl_label = "Grab Assist Operator"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: GrabAssist: loaded.")

    def execute(self, context):
        print("MMZ Add-on: GrabAssist: running.")

        def Grab(self, context):
            #軸の設定を取得
            pos = (
                bpy.context.scene.grab_pro.dir_x,
                bpy.context.scene.grab_pro.dir_y,
                bpy.context.scene.grab_pro.dir_z
            )

            bpy.ops.transform.translate("INVOKE_DEFAULT", constraint_axis=(pos[0], pos[1], pos[2]))

        if len(bpy.context.selected_objects) > 0:
            if bpy.context.scene.grab_pro.slide:
                if bpy.context.object.mode == "EDIT":
                    bpy.ops.transform.vert_slide("INVOKE_DEFAULT")
                else: Grab(self, context)
            else:
                Grab(self, context)

        return {"FINISHED"}
    
class RotateAssistOperator(bpy.types.Operator):
    bl_idname = "mmz.rotateassist_operator"
    bl_label = "Rotate Assist Operator"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: RotateAssist: loaded.")

    def execute(self, context):
        print("MMZ Add-on: RotateAssist: running.")

        def Rotate(self, context):
            #軸の設定を取得
            pos = (
                bpy.context.scene.rotate_pro.dir_x,
                bpy.context.scene.rotate_pro.dir_y,
                bpy.context.scene.rotate_pro.dir_z
            )
            bpy.ops.transform.rotate("INVOKE_DEFAULT", constraint_axis=(pos[0], pos[1], pos[2]))

        if len(bpy.context.selected_objects) > 0:
            Rotate(self, context)

        return {"FINISHED"}

def register():
    bpy.utils.register_class(GrabAssistOperator)
    bpy.utils.register_class(RotateAssistOperator)
def unregister():
    bpy.utils.unregister_class(GrabAssistOperator)
    bpy.utils.unregister_class(RotateAssistOperator)
if __name__ == "__main__":
    register()
