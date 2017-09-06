A glance of application microoh.com
=======================================

index::

    apps：              # 自己开发的APP目录
    conf:               # 服务器配置文件目录
    docs：              # API文档目录
    extra_apps:         # 第三方APP
    libs：              # 第三方依赖库目录
    maiziedu_website:   # web工程目录
    static：            # 静态文件资源目录
    templates：         # 模板目录
    templatetags：      # tag目录
    tests：             # 单元测试目录
    upload：            # 上传目录  （目录及其子目录都需要写入权限，重要）
    utils              # 工具类目录

trigger::

    #同步回帖发帖等论坛消息的触发器
    create trigger tg_notification
    after insert on pre_home_notification
    for each row
    begin
    set @userA_uid=new.authorid;
    set @userB_uid=new.uid;
    set @userA_id=(select id from maiziedu_website.mz_user_userprofile where uid=@userA_uid);
    set @userB_id=(select id from maiziedu_website.mz_user_userprofile where uid=@userB_uid);
    insert into maiziedu_website.mz_common_mymessage(userA,userB,action_type,action_id,action_content,date_action,is_new) values(@userA_id,@userB_id,'3',new.id,new.note,now(),1);
    end;

