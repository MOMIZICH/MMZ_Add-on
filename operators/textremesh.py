import bpy

class TextRemeshOperator(bpy.types.Operator):
    bl_idname = "mmz.textremesh_operator"
    bl_label = "Text Remesh Operator"
    bl_description = "テキストを選択して実行するとメッシュに変換します"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: TextRemesh: loaded.")

    def execute(self, context):
        print("MMZ Add-on: TextRemesh: loaded.")

        
        selected_obj = bpy.context.selected_objects #選択してたオブジェクトの保存
        
        if selected_obj:
            used_mode = context.object.mode
            if used_mode == "EDIT":
                pass
            elif used_mode == "OBJECT":
                bpy.ops.object.mode_set(mode = "EDIT")
            else:
                print("MMZ Add-on: TextRemesh: Error: Unavailable Mode.")
                return{"CANCELLED"}
                
            #選択していたオブジェクトの保存
            active_obj = bpy.context.active_object #アクティブオブジェクトの保存
            selected_text = []
            for obj in selected_obj: #テキスト以外の選択解除
                if obj.type == "FONT":
                    selected_text.append(obj)

            for obj in selected_text:
                bpy.ops.object.mode_set(mode = "OBJECT")
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.convert(target='MESH')
                bpy.ops.object.mode_set(mode = "EDIT")
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.1), "orient_type": "NORMAL"})
                remesh_mod = obj.modifiers.new(name="Remesh", type="REMESH")
                remesh_mod.mode = "SHARP"
                remesh_mod.octree_depth = 8
                remesh_mod.use_remove_disconnected = False
                bpy.ops.object.mode_set(mode = "OBJECT")
                bpy.ops.object.modifier_apply({"object": obj}, modifier="Remesh")
                bpy.ops.object.mode_set(mode = "EDIT")
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.mesh.dissolve_limited()

                if used_mode == "OBJECT":
                    bpy.ops.object.mode_set(mode = "OBJECT")

                # vertex_list = []
                # for v in obj.vertices:
                #     vertex_list.append(v.index)

        return{"FINISHED"}

def register():
    bpy.utils.register_class(TextRemeshOperator)
def unregister():
    bpy.utils.unregister_class(TextRemeshOperator)
