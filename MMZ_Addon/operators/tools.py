import bpy
import mathutils


class GetMiddleToOriginOperator(bpy.types.Operator):
    bl_idname = "mmz.getmiddletoorigin_operator"
    bl_label = "Get Middle to Origin Operator"
    bl_description = "選択されている頂点を原点に設定します。複数の頂点が選択されている場合はそれらの中点を原点にします"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: GetMiddlePoint: loaded.")

    def execute(self, context):
        print("MMZ Add-on: GetMiddlePoint: running.")

        
        if bpy.context.object:
            select_mode = bpy.context.tool_settings.mesh_select_mode[:]
            bpy.context.tool_settings.mesh_select_mode = [True, False, False]
            used_mode = bpy.context.object.mode

            if used_mode == "EDIT":
                bpy.ops.object.mode_set(mode = "OBJECT")
                bpy.ops.object.mode_set(mode = "EDIT")
            elif used_mode == "OBJECT":
                bpy.ops.object.mode_set(mode = "EDIT")
                bpy.ops.object.mode_set(mode = "OBJECT")
                bpy.ops.object.mode_set(mode = "EDIT")
            else:
                print("MMZ Add-on: GetMiddlePoint: Error: Unavailable Mode.")
                return{"CANCELLED"}

            obj = bpy.context.active_object
            mesh = obj.data

            selected_verts = []
            for v in mesh.vertices:
                if v.select:
                    selected_verts.append(v)

            if selected_verts:
                total = mathutils.Vector()
                for v in selected_verts:
                    total += v.co
                midpoint = total / len(selected_verts)

                bpy.ops.object.mode_set(mode = "OBJECT")

                global_mid = obj.matrix_world @ midpoint
                cursor = bpy.context.scene.cursor
                pos = cursor.location.copy()
                cursor.location = global_mid
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                print(f"MMZ Add-on: GetMiddlePoint: Move object({obj.name}) origin to {global_mid}")
                cursor.location = pos

                if used_mode == "EDIT":
                    bpy.ops.object.mode_set(mode = "EDIT")
            else:
                print("MMZ Add-on: GetMiddlePoint: Error: No selected vertex.")
                return{"CANCELLED"}
            
            bpy.context.tool_settings.mesh_select_mode = select_mode

        return{"FINISHED"}
    
class ApplyAllModifierOperator(bpy.types.Operator):
    bl_idname = "mmz.applymodifier_operator"
    bl_label = "Apply All Modifier Operator"
    bl_description = "メッシュオブジェクトのモディファイアーをすべて適用します。"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: ApplyAllModifier: loaded.")

    def execute(self, context):
        print("MMZ Add-on: ApplyAllModifier: running.")

        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        used_mode = bpy.context.object.mode

        if used_mode == "EDIT":
            bpy.ops.object.mode_set(mode = "OBJECT")
        elif used_mode == "OBJECT":
            pass
        else:
            print("MMZ Add-on: AutoMarge: Error: Unavailable Mode.")
            return{"CANCELLED"}

        if selected_obj:
            for obj in selected_obj:
                if obj.type == "MESH":
                    bpy.context.view_layer.objects.active = obj
                    if obj.modifiers:
                        for mod in obj.modifiers:
                            bpy.ops.object.modifier_apply(modifier=mod.name)

        if active_obj:
            bpy.context.view_layer.objects.active = active_obj
        if used_mode == "EDIT":
            bpy.ops.object.mode_set(mode = "EDIT")

        return{"FINISHED"}
    
class AddBooleanOperator(bpy.types.Operator):
    bl_idname = "mmz.addboolean_operator"
    bl_label = "Add Buolean Operator"
    bl_description = "アクティブオブジェクトにブーリアンモディファイアーを追加し、もう一方を演算対象に指定します。"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: AddBoolean: loaded.")

    def execute(self, context):
        print("MMZ Add-on: AddBoolean: running.")

        selected_obj = bpy.context.selected_objects #選択しているオブジェクト
        bool_pri = bpy.context.active_object #アクティブオブジェクト(モディファイアー掛ける方)
        mode = bpy.context.scene.addbool.mode #モードの列挙型プロパティ

        #ブーリアン対象を取得
        bool_target = [] #ブーリアンを掛けられる側
        for obj in selected_obj: #オブジェクトごとにループ(2回)
            if not obj == bool_pri: #アクティブオブジェクトでないなら
                bool_target.append(obj) #bool_targetに追加
        bool_target = bool_target[0] #リストじゃだめらしいので
        
        #モディファイアー
        bool_mod = bool_pri.modifiers.new("MMZ_bool", "BOOLEAN") #ブーリアンモディファイアー追加
        bool_mod.object = bool_target #対象オブジェクトにbool_targetを指定
        bool_mod.operation = mode #実行モードを指定

        collection_name = "MMZ_Boolean_Collections" #対象オブジェクトを入れるコレクション
        if collection_name in bpy.data.collections: #コレクションが存在したら何もしない
            pass
        else: #なかったら作ってアウトライナーにリンクする
            new_collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(new_collection)
        
        target_name_old = str(bool_target.name) #対象オブジェクトの旧名を取得
        target_name = f"MMZ_Bool:{target_name_old}/Mode:{mode}" #新しい名前

        if mode == "DIFFERENCE": #差分モードだったら
            bpy.data.objects[target_name_old].display_type = "WIRE" #対象オブジェクトをワイヤーフレーム表示に
        elif mode =="UNION": #合成モードだったら
            bpy.data.objects[target_name_old].hide_viewport = True #対象オブジェクトを非表示に(アウトライナーからは弄れない)
            bpy.data.objects[target_name_old].hide_render = True #レンダリングしない
        elif mode == "INTERSECT": #交差モードだったら
            bpy.data.objects[target_name_old].hide_viewport = True #対象オブジェクトを非表示に(アウトライナーからは弄れない)
            bpy.data.objects[target_name_old].hide_render = True #レンダリングしない
            
        bpy.data.objects[target_name_old].name = target_name #対象オブジェクトを改名
        collection = bpy.data.collections[collection_name] #コレクションを取得
        collection.objects.link(bool_target) #コレクションに追加
        bpy.context.scene.collection.objects.unlink(bool_target) #昔のコレクションを切る
        
        return{"FINISHED"}
    
class WireFrameSwitchOperator(bpy.types.Operator):
    bl_idname = "mmz.wireframeswitch_operator"
    bl_label = "Wire Frame Switch Operator"
    bl_description = "ワイヤーフレーム表示とテクスチャ表示を切り替えます。それ以外だった場合はワイヤーフレームになります。"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: WireFrameSwitch: loaded.")

    def execute(self, context):
        print("MMZ Add-on: WireFrameSwitch: running.")

        selected_obj = bpy.context.selected_objects
        if selected_obj:
            for obj in selected_obj:
                if obj.display_type == "WIRE":
                    obj.display_type = "TEXTURED"
                else:
                    obj.display_type = "WIRE"

        return{"FINISHED"}



def register_classes():
    classes = [
        GetMiddleToOriginOperator,
        ApplyAllModifierOperator,
        AddBooleanOperator,
        WireFrameSwitchOperator
    ]
    return classes

def register():
    classes = register_classes()
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    classes = register_classes()
    for cls in classes:
        bpy.utils.unregister_class(cls)
if __name__ == "__main__":
    register()