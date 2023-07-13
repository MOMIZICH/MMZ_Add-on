import bpy

class TextSenderOperator(bpy.types.Operator):
    bl_idname = "mmz.textsender_operator"
    bl_label = "Text Sender Operator"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: TextSender: loaded.")

    def execute(self, context):
        print("MMZ Add-on: TextSender: running.")

        if not bpy.context.scene.textsender.text: #textプロパティが空なら終わる
            print("MMZ Add-on: TextSender: Error: Text isn't exist.")
            return{"CANCELLED"}
        
        active_obj = bpy.context.active_object
        text = bpy.context.scene.textsender.text
        if active_obj: #アクティブオブジェクトが選択されていたら
            if not active_obj.type == "FONT": #アクティブオブジェクトがテキストオブジェクトでないなら
                bpy.ops.object.text_add() #テキストオブジェクトを追加する
                active_obj = bpy.context.active_object #テキストオブジェクトをactive_objに取得
                active_obj.data.body = "" #文字を空にする
        else:
            bpy.ops.object.text_add()
            active_obj = bpy.context.active_object
            active_obj.data.body = ""

        if bpy.context.scene.textsender.line_mode == "new_line": #改行モードが有効なら
            previous = active_obj.data.body #テキストオブジェクトの文字を取得する
            if previous: #文字があったら
                active_obj.data.body = previous + f"\n" + text #改行して追加する
            else: #なければ
                active_obj.data.body = text #そのまま追加する
        else:
            active_obj.data.body = text

        bpy.context.scene.textsender.text = "" #textプロパティを空にする
                
        return{"FINISHED"}
    
class GetPreviousTextOperator(bpy.types.Operator):
    bl_idname = "mmz.getprevioustext_operator"
    bl_label = "Get Grevious Text Operator"
    bl_options = {"REGISTER", "UNDO"}

    print("MMZ Add-on: GetPreviousText: loaded.")

    def execute(self, context):
        print("MMZ Add-on: GetPreviousText: ran.")

        active_obj = bpy.context.active_object #アクティブオブジェクトを取得
        if not active_obj and active_obj.type == "FONT": #アクティブオブジェクトが無い&テキストでないなら
            return{"CANCELLED"} #終わる
        bpy.context.scene.textsender.text = bpy.context.active_object.data.body #テキストオブジェクトの内容をtextに反映
        return{"FINISHED"}
        

def register():
    bpy.utils.register_class(TextSenderOperator)
    bpy.utils.register_class(GetPreviousTextOperator)
def unregister():
    bpy.utils.unregister_class(TextSenderOperator)
    bpy.utils.unregister_class(GetPreviousTextOperator)
if __name__ == "__main__":
    register()