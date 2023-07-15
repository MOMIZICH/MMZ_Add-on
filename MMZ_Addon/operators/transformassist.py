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
            pos = {"x": False, "y": False, "z": False}
            dir = bpy.context.scene.grab_pro.dir
            if "x" in dir:
                pos["x"] = True
            if "y" in dir:
                pos["y"] = True
            if "z" in dir:
                pos["z"] = True
            if pos["x"] == pos["y"] == pos["z"] == False:
                raise RuntimeError("MMZ Add-on: GrabAssist: Error: Nothing has been selected.")

            bpy.ops.transform.translate("INVOKE_DEFAULT", constraint_axis=(pos["x"], pos["y"], pos["z"]))

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
            pos = {"x": False, "y": False, "z": False}
            dir = bpy.context.scene.grab_pro.dir
            
            if "x" in dir:
                pos["x"] = True
            if "y" in dir:
                pos["y"] = True
            if "z" in dir:
                pos["z"] = True
            if pos["x"] == pos["y"] == pos["z"] == False:
                raise RuntimeError("MMZ Add-on: RotateAssist: Error: Nothing has been selected.")
            
            bpy.ops.transform.rotate("INVOKE_DEFAULT", constraint_axis=(pos["x"], pos["y"], pos["z"]))

        if len(bpy.context.selected_objects) > 0:
            Rotate(self, context)

        return {"FINISHED"}
    
class ResizeAssistOperator(bpy.types.Operator):
    bl_idname = "mmz.resizeassist_operator"
    bl_label = "Resize Assist Operator"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: ResizeAssist: loaded.")

    def execute(self, context):
        print("MMZ Add-on: ResizeAssist: running.")
        
        def Resize(self, context):
            #軸の設定を取得
            pos = {"x": False, "y": False, "z": False}
            dir = bpy.context.scene.grab_pro.dir
            
            if "x" in dir:
                pos["x"] = True
            if "y" in dir:
                pos["y"] = True
            if "z" in dir:
                pos["z"] = True
            if pos["x"] == pos["y"] == pos["z"] == False:
                raise RuntimeError("MMZ Add-on: ResizeAssist: Error: Nothing has been selected.")

            bpy.ops.transform.resize("INVOKE_DEFAULT", constraint_axis=(pos["x"], pos["y"], pos["z"]))

        if len(bpy.context.selected_objects) > 0:
            Resize(self, context)

        return {"FINISHED"}

def register():
    bpy.utils.register_class(GrabAssistOperator)
    bpy.utils.register_class(RotateAssistOperator)
    bpy.utils.register_class(ResizeAssistOperator)
def unregister():
    bpy.utils.unregister_class(GrabAssistOperator)
    bpy.utils.unregister_class(RotateAssistOperator)
    bpy.utils.unregister_class(ResizeAssistOperator)
if __name__ == "__main__":
    register()
