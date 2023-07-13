import bpy

class MMZ_MT_AddonMenu(bpy.types.Menu):
    bl_label = "トランスフォームアシスト"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        scene = context.scene

        group1 = pie.split().column()
        group1.label(text="移動アシスト")
        group1.label(text="軸を指定")
        group1.prop(scene.grab_pro, "dir_x")
        group1.prop(scene.grab_pro, "dir_y")
        group1.prop(scene.grab_pro, "dir_z")
        
        group1.label(text="有効化")
        group1.prop(scene.grab_pro, "enabled", text="モードを有効にする")
        group1.prop(scene.grab_pro, "slide", text="エッジスライドを有効にする")
        group1.prop(scene.grab_pro, "multi", text="複数の軸を有効にする")


        group2 = pie.split().column()
        group2.label(text="回転アシスト")
        group2.label(text="軸を指定")
        group2.prop(scene.rotate_pro, "dir_x")
        group2.prop(scene.rotate_pro, "dir_y")
        group2.prop(scene.rotate_pro, "dir_z")

        group2.label(text="有効化")
        group2.prop(scene.rotate_pro, "enabled", text="モードを有効にする")
        group2.prop(scene.rotate_pro, "multi", text="複数の軸を有効にする")

class AddonPieMenu_Call(bpy.types.Operator):
    bl_idname = "mmz.addonmenu_piemenu_call"
    bl_label = "パイメニューを呼び出す"
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="MMZ_MT_AddonMenu")
        return {"FINISHED"}

def register():
    bpy.utils.register_class(MMZ_MT_AddonMenu)
    bpy.utils.register_class(AddonPieMenu_Call)
def unregister():
    bpy.utils.unregister_class(MMZ_MT_AddonMenu)
    bpy.utils.unregister_class(AddonPieMenu_Call)

if __name__ == "__main__":
    register()