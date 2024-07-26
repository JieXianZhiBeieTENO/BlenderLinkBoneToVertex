bl_info = {
    "name" : "骨骼选择性绑定",
    "author" : "尐贤之辈のTENO",
    "description" : "效率指定骨骼绑定",
    "blender" : (3, 3, 0),
    "version" : (1, 0, 0),
    "location" : "View 3D > bo_link",
    "warning" : "这是本人第三次制作插件，如有问题也请多多包涵╭(╰▽╯)╮",
    "category" : "Bones",
    "doc_url": "",
    "tracker_url": "https://space.bilibili.com/1729654169"
}
import bpy,json,blf,bpy_extras
from bpy.props import (
        IntProperty,
        BoolProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty,
        FloatProperty,
        IntVectorProperty,
        EnumProperty,
        CollectionProperty
    )
class Ve(bpy.types.Operator):
    bl_idname="bo_link.sp_ve"
    bl_label="顶点组生成"
    bl_options={"REGISTER","UNDO"}
    bl_description="为每个被选中物体的顶点分组"
    def execute(self,context):
        for i in bpy.context.selected_objects:
            for c,o in enumerate(i.data.vertices):
                i.vertex_groups.new(name=str(c)).add([c],1,"ADD")
        return {"FINISHED"}

def bo_spawn():
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass
    bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.object.name="link"
    bpy.context.object.data.name="link"
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.object.data.edit_bones.remove(bpy.context.object.data.edit_bones[0])

class link(bpy.types.Operator):
    bl_idname="bo_link.link"
    bl_label="绑定"
    bl_options={"REGISTER","UNDO"}
    def execute(self,context):
        tools=context.scene.bo_link
        if tools.Type=="more":
            L=tools.more_Ob
        elif tools.Type=="one":
            L=tools.one_Ob
        else:
            L=context.selected_objects
        if tools.Type=="zero" and bool(L):
            bo_spawn()
            for c,i in enumerate(L):
                bone=bpy.context.object.data.edit_bones.new(name=str(c))
                bone.head, bone.tail = (0,)*3, (0,0,1)
                bpy.ops.object.mode_set(mode='POSE')
                bpy.context.object.pose.bones[str(c)].constraints.new("COPY_LOCATION").target=i
                bpy.context.object.pose.bones[str(c)].constraints.new("COPY_ROTATION").target=i
                bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode='OBJECT')
            return {"FINISHED"}
        for i in L:
            if bool(i.f_ob):
                bo_spawn()
                if tools.Type=="more":
                    for c,i in enumerate(tools.more_Ob):
                        if not i.f_ob is None:
                            bone=bpy.context.object.data.edit_bones.new(name=str(c))
                            bone.head, bone.tail = (0,)*3, (0,0,1)
                            bpy.ops.object.mode_set(mode='POSE')
                            Con=bpy.context.object.pose.bones[str(c)].constraints.new("COPY_LOCATION")
                            Con.target=i.f_ob
                            Con.subtarget=i.f_ve
                            if not i.f_ve is None:
                                Con=bpy.context.object.pose.bones[str(c)].constraints.new("DAMPED_TRACK")
                                Con.target=i.e_ob
                                Con.subtarget=i.e_ve
                            bpy.ops.object.mode_set(mode='EDIT')
                elif tools.Type=="one":
                    for c,i in enumerate(tools.one_Ob):
                        if not i.f_ob is None:
                            bone=bpy.context.object.data.edit_bones.new(name=str(c))
                            bone.head, bone.tail = (0,)*3, (0,0,1)
                            bpy.ops.object.mode_set(mode='POSE')
                            Con=bpy.context.object.pose.bones[str(c)].constraints.new("COPY_LOCATION")
                            Con.target=i.f_ob
                            Con.subtarget=i.f_ve
                            if not tools.T_ob is None:
                                Con=bpy.context.object.pose.bones[str(c)].constraints.new("DAMPED_TRACK")
                                Con.target=tools.T_ob
                                Con.subtarget=tools.T_ve
                            bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='OBJECT')
                return {"FINISHED"}
    
class ad_sel_ve(bpy.types.Operator):
    bl_idname="bo_link.ad_sel_ve"
    bl_label="添加选中顶点"
    bl_options={"REGISTER","UNDO"}
    def execute(self,context):
        bpy.ops.object.mode_set(mode='OBJECT')
        cou=1
        tools=context.scene.bo_link
        if tools.Type=="more":
            T=context.scene.bo_link.more_Ob
        elif tools.Type=="one":
            T=context.scene.bo_link.one_Ob
        for i in context.object.data.vertices:
            if cou:
                T.add()
                cou=0
            if i.select:
                T[-1].f_ob=context.object
                T[-2].f_ve=str(i.index)
        bpy.ops.object.mode_set(mode='EDIT')
        return {"FINISHED"}

class remove_all(bpy.types.Operator):
    bl_idname="bo_link.remove_all"
    bl_label="移除全部"
    bl_options={"REGISTER","UNDO"}
    def execute(self,context):
        tools=context.scene.bo_link
        if tools.Type=="more":
            T=context.scene.bo_link.more_Ob
        elif tools.Type=="one":
            T=context.scene.bo_link.one_Ob
        T.clear()
        return {"FINISHED"}
    
class f_add(bpy.types.Operator):
    bl_idname="bo_link.f_add"
    bl_label="添加初始量"
    bl_options={"REGISTER","UNDO"}
    def execute(self,context):
        tools=context.scene.bo_link
        if tools.Type=="more":
            tools.more_Ob.add()
        if tools.Type=="one":
            tools.one_Ob.add()
        return {"FINISHED"}
    
def Add(self,context):
    tools=context.scene.bo_link
    if bool(tools.more_Ob):
        if bool(tools.more_Ob[len(tools.more_Ob)-1].f_ob):
            tools.more_Ob.add()
    if bool(tools.one_Ob):
        if bool(tools.one_Ob[len(tools.one_Ob)-1].f_ob):
            tools.one_Ob.add()
def Rem(self,context):
    tools=context.scene.bo_link
    if tools.Type=="more":
        for c,i in enumerate(tools.more_Ob):
            if i.rem:
                tools.more_Ob.remove(c)
    elif tools.Type=="one":
        for c,i in enumerate(tools.one_Ob):
            if i.rem:
                tools.one_Ob.remove(c)
def Ret(self,context):
    tools=context.scene.bo_link
    if tools.Type=="more":
        for c,i in enumerate(tools.more_Ob):
            if i.ret_f and c:
                i.f_ob=tools.more_Ob[c-1].f_ob
                i.ret_f=False
            if i.ret_e and c:
                i.e_ob=tools.more_Ob[c-1].e_ob
                i.ret_e=False
    elif tools.Type=="one":
        for c,i in enumerate(tools.one_Ob):
            if i.ret_f and c:
                i.f_ob=tools.one_Ob[c-1].f_ob
                i.ret_f=False
                
                
class MOTIONCATCH_MT_Error_menu(bpy.types.Menu):
    bl_label = "错误"
    bl_idname = "MOTIONCATCH_MT_Error_menu"

    def draw(self, context):
        tools=context.scene.bo_link
        layout = self.layout
        layout.label(text=tools.error_thing,icon="ERROR")

    def draw_item(self, context):
        layout = self.layout
        layout.menu(MOTIONCATCH_MT_Error_menu.bl_idname)
def rl(naming=MOTIONCATCH_MT_Error_menu):
    bpy.ops.wm.call_menu(name=naming.bl_idname)
    
    
def give_index(self,context):
    tools=context.scene.bo_link
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    if tools.Type=="one":
        for i in tools.one_Ob:
            if i.f_give_index:
                for o in i.f_ob.data.vertices:
                    if o.select:
                        if not context.mode=='EDIT_MESH':
                            bpy.ops.object.mode_set(mode='EDIT')
                        i.f_ve=str(o.index)
                        i.f_give_index=False
                        break
                    else:
                        i.f_give_index=False
    else:
        for i in tools.more_Ob:
            if i.f_give_index:
                for o in i.f_ob.data.vertices:
                    if o.select:
                        if not context.mode=='EDIT_MESH':
                            bpy.ops.object.mode_set(mode='EDIT')
                        i.f_ve=str(o.index)
                        i.f_give_index=False
                        break
                    else:
                        i.f_give_index=False
            elif i.e_give_index:
                for o in i.e_ob.data.vertices:
                    if o.select:
                        if not context.mode=='EDIT_MESH':
                            bpy.ops.object.mode_set(mode='EDIT')
                        i.e_ve=str(o.index)
                        i.e_give_index=False
                        break
                    else:
                        i.e_give_index=False
    
class more_Vars(bpy.types.PropertyGroup):
    f_ob: PointerProperty(type=bpy.types.Object,update=Add)
    e_ob: PointerProperty(type=bpy.types.Object)
    f_ve: StringProperty()
    e_ve: StringProperty()
    rem: BoolProperty(update=Rem)
    ret_f: BoolProperty(update=Ret)
    ret_e: BoolProperty(update=Ret)
    f_give_index: BoolProperty(update=give_index)
    e_give_index: BoolProperty(update=give_index)
    
class one_Vars(bpy.types.PropertyGroup):
    f_ob: PointerProperty(type=bpy.types.Object,update=Add)
    f_ve: StringProperty()
    rem: BoolProperty(update=Rem)
    ret_f:BoolProperty(update=Ret)
    f_give_index: BoolProperty(update=give_index)
        
def draw_callback_px(self, context):
    tools=context.scene.bo_link
    region=context.region
    space_data=context.space_data.region_3d
    for ob in context.selected_objects:
        for v in ob.data.vertices:
            l=ob.matrix_world@v.co
            view_draw=bpy_extras.view3d_utils.location_3d_to_region_2d(region,space_data,l)
            blf.size(0, tools.text_size)
            blf.color(0,tools.te_col[0],tools.te_col[1],tools.te_col[2],1)
            blf.position(0, view_draw[0], view_draw[1],0)
            blf.draw(0,str(v.index))
                
def show_text(self,context):
    tools=context.scene.bo_link
    if tools.is_show_text:
        bpy.types.Scene.bo_link_textshow_info = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL') 
    else:
        bpy.types.SpaceView3D.draw_handler_remove(bpy.types.Scene.bo_link_textshow_info,'WINDOW')
             
class Var(bpy.types.PropertyGroup):
    Type: EnumProperty(
        name="阻尼目标",
        items=(
            ("zero","无",""),
            ("one", "单个", ""),
            ("more", "多个", ""),
        ),
        default="more",
    )
    more_Ob: CollectionProperty(type=more_Vars)
    
    one_Ob: CollectionProperty(type=one_Vars)
    T_ob: PointerProperty(type=bpy.types.Object)
    T_ve: StringProperty()
    
    is_show_te_pa: BoolProperty(name="显示顶点编号面板")
    text_size: FloatProperty(name="字体大小",default=20)
    is_show_text: BoolProperty(name="显示顶点编号",update=show_text)
    te_col: FloatVectorProperty(name="字体颜色",subtype="COLOR",soft_max=1,soft_min=0)
    
    error_thing: StringProperty()

class spawn_ob_bo_link(bpy.types.Operator):
    bl_idname="bo_link.spawn_ob_bo_link"
    bl_label="批量绑定骨骼"
    bl_options={"REGISTER","UNDO"}
    bl_description="注:仅绑定骨骼父级，不增加顶点组与修改器"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self,context):
        tools=context.scene.bo_link
        se=context.selected_objects
        se.remove(context.object)
        ar=context.object
        if len(se)>1:
            tools.error_thing="选择了不止一个非活动物体"
            rl()
            return {"FINISHED"}
        elif len(se)==0:
            tools.error_thing="只选择了一个物体"
            rl()
            return {"FINISHED"}
        if not(bool(context.object.data) and str(context.object.data)[13:21]=='Armature'):
            tools.error_thing="活动物体非骨骼"
            rl()
            return {"FINISHED"}
        bpy.ops.object.select_all(action='DESELECT')
        se[0].select_set(True)
        for i in ar.data.bones:
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            bpy.ops.object.location_clear(clear_delta=False)
            bpy.ops.object.rotation_clear(clear_delta=False)
            bpy.ops.object.scale_clear(clear_delta=False)
            sel=context.selected_objects[0]
            sel.parent=ar
            sel.parent_type='BONE'
            sel.parent_bone=i.name
        return {"FINISHED"}

class BO_LINK_PT_pa_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Boneslink"
    bl_idname = "BO_LINK_PT_pa_panel"
    bl_label = "骨骼选择性绑定"
    def draw(self,context):
        layout=self.layout
        tools=context.scene.bo_link
        col=layout.column(align=True)
        col.operator(Ve.bl_idname)
        col.label(text="-"*30)
        col.column().prop(tools,'is_show_te_pa',icon="TRIA_DOWN" if tools.is_show_te_pa else "TRIA_RIGHT")
        if tools.is_show_te_pa:
            col.prop(tools,'is_show_text',icon="FILE_TEXT")
            col.prop(tools,'te_col')
            col.prop(tools,"text_size")
        col.label(text="-"*30)
        col.prop(tools,"Type")
        boxx=layout.column().box().row(align=True)
        if (len(tools.one_Ob)==0 and tools.Type=="one") or (len(tools.more_Ob)==0 and tools.Type=="more"):
            boxx.operator(f_add.bl_idname)
        else:
            boxx.operator(link.bl_idname)
        if tools.Type!="zero":
            boxx.operator(ad_sel_ve.bl_idname,text="",icon="LINKED")
        if tools.Type=="one":
            boxz=layout.row().box().row(align=True)
            boxz.label(text="阻尼跟踪物体")
            boxz.prop(tools,"T_ob",text="")
            if not tools.T_ob is None and not tools.T_ob.data is None and str(tools.T_ob.data)[13:17]=='Mesh':
                boxz.prop_search(tools,"T_ve",tools.T_ob,"vertex_groups",icon="GROUP_VERTEX",text="")
            boxx=layout.column().box().column(align=True)
            boxx.label(text="复制位置物体")
            te="#单阻尼绑定面板"
            box0=boxx.row(align=True)
            if not bool(tools.one_Ob):
                boxx.label(text="       请点击“添加初始量”")
            for c,i in enumerate(tools.one_Ob):
                exec(f'''
global box{str(c+1)}
if c:
    box{str(c)}.prop(i,"ret_f",text="",icon="TRIA_RIGHT")
else:
    box{str(c)}.label(text="",icon="CUBE")
box{str(c)}.prop(i,"f_ob",text="")
if not i.f_ob is None and not i.f_ob.data is None and str(i.f_ob.data)[13:17]=='Mesh':
    box{str(c)}.prop_search(i,"f_ve",i.f_ob,"vertex_groups",icon="GROUP_VERTEX",text="")
    box{str(c)}.prop(i,"f_give_index",text="",icon="EYEDROPPER")
box{str(c)}.prop(i,"rem",text="",icon="REMOVE")
box{str(c+1)}=boxx.row(align=True)
                ''')
            if bool(tools.one_Ob):
                list_rem=boxx.column(align=True)
                list_rem.label(text="═"*10)
                list_rem1=list_rem.row()
                list_rem1.label(text="═"*5)
                list_rem1.operator(remove_all.bl_idname,icon="REMOVE")
                
        elif tools.Type=="more":
            te="#多阻尼绑定面板"
            boxx=layout.column().box().column(align=True)
            boxx.label(text="复制位置+阻尼跟踪物体")
            if not bool(tools.more_Ob):
                boxx.label(text="       请点击“添加初始量”")
            box0=boxx.row(align=True)
            for c,i in enumerate(tools.more_Ob):
                exec(f'''
global box{str(c+1)}
if c:
    box{str(c)}.prop(i,"ret_f",text="",icon="TRIA_RIGHT")
else:
    box{str(c)}.label(text="",icon="CUBE")
box{str(c)}.prop(i,"f_ob",text="")
if not i.f_ob is None and not i.f_ob.data is None and str(i.f_ob.data)[13:17]=='Mesh':
    box{str(c)}.prop_search(i,"f_ve",i.f_ob,"vertex_groups",icon="GROUP_VERTEX",text="")
    box{str(c)}.prop(i,"f_give_index",text="",icon="EYEDROPPER")
box{str(c)}.label(text="",icon="FORWARD")
if c:
    box{str(c)}.prop(i,"ret_e",text="",icon="TRIA_RIGHT")
box{str(c)}.prop(i,"e_ob",text="")
if not i.e_ob is None and not i.e_ob.data is None and str(i.e_ob.data)[13:17]=='Mesh':
    box{str(c)}.prop_search(i,"e_ve",i.e_ob,"vertex_groups",icon="GROUP_VERTEX",text="")
    box{str(c)}.prop(i,"e_give_index",text="",icon="EYEDROPPER")
box{str(c)}.prop(i,"rem",text="",icon="REMOVE")
box{str(c+1)}=boxx.row(align=True)
                ''')
            if bool(tools.more_Ob):
                list_rem=boxx.column(align=True)
                list_rem.label(text="═"*12)
                list_rem1=list_rem.row()
                list_rem1.label(text="═"*12)
                list_rem1.operator(remove_all.bl_idname,icon="REMOVE")
            
            
        else:
            te="请选择需绑定复制位置和复制旋转的物体（可多选）"
        
        boox=layout.row().box().column()
        if bool(context.selected_objects):
            boox.enabled=True
        else:
            boox.enabled=False
            boox.label(text="请选择物体")
        boox.operator(spawn_ob_bo_link.bl_idname)
        
        layout.label(text=te)
        
cls=(Ve,
    f_add,
    one_Vars,
    more_Vars,
    link,
    Var,
    ad_sel_ve,
    remove_all,
    MOTIONCATCH_MT_Error_menu,
    spawn_ob_bo_link,
    BO_LINK_PT_pa_panel)

def register():
    for cl in cls:
        bpy.utils.register_class(cl)
    bpy.types.Scene.bo_link=bpy.props.PointerProperty(type=Var)
def unregister():
    for cl in cls:
        bpy.utils.unregister_class(cl)
    del bpy.types.Scene.bo_link
if __name__=="__main__":
    register()
            
            
    