apps��              �Լ�������APPĿ¼
conf:               �����������ļ�Ŀ¼
docs��              API�ĵ�Ŀ¼
extra_apps:         ������APP
libs��              ������������Ŀ¼
maiziedu_website:   web����Ŀ¼
static��            ��̬�ļ���ԴĿ¼
templates��         ģ��Ŀ¼
templatetags��      tagĿ¼
tests��             ��Ԫ����Ŀ¼
upload��            �ϴ�Ŀ¼  ��Ŀ¼������Ŀ¼����Ҫд��Ȩ�ޣ���Ҫ��
utils��             ������Ŀ¼


//ͬ��������������̳��Ϣ�Ĵ�����
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
