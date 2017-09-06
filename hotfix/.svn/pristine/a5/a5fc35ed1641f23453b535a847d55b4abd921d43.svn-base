# -*- coding: utf-8 -*-
CAREERS = """
    {% if careers %}
        {% for c in careers %}
            {% if career_id == c.id %}
                <li class="select"><a>{{ c.name }}</a></li>
            {% else %}
                <li><a href="{% url 'lps4_index' c.id %}">{{ c.name }}</a></li>
            {% endif %}
        {% endfor %}
    {% endif %}
"""
STAGES = """
    {% for stage in stages %}
        <div class="study-stage study-stage-1">
            <div class="study-stage-progress">
                <div class="progress-on"></div>
            </div>
            <div class="study-stage-box">
                <h2>{{ stage.name }}</h2>
                <div class="study-stage-ball">
                    <ul class="lists">
                        {% for task in stage.tasks %}
                            {% if task.is_done %}
                                <li class="score" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span></span>
                                        <p attr-a="" attr-b="评分中" color-a="green" color-b=""
                            {% elif task.is_pass %}
                                <li class="finish" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span></span>
                                        <p attr-a="" attr-b="已完成" color-a="orange" color-b=""
                            {% elif task.is_fail %}
                                <li class="rebuild" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span></span>
                                        <p attr-a="" attr-b="成绩不合格请重修" color-a="red" color-b=""
                            {% elif task.is_redoing %}
                                <li class="rebuilding" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span><i></i></span>
                                        <p attr-a="" attr-b="课程重修中" color-a="green" color-b=""
                            {% elif task.task_show_status == 1 %}
                                <li class="ongoing" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span></span>
                                        <p left-time="{{ task.get_timeleft }}"
                                           attr-b="正在学习（{{ task.get_progress }}%）" color-a="green"
                                           color-b="dark-green"
                            {% elif task.task_show_status == 2 %}
                                <li class="ongoing cutdwon-oneday" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span><i></i></span>
                                        <p attr-a="已超时" attr-b="正在学习（{{ task.get_progress }}%）" color-a="green"
                                           color-b="orange"
                            {% elif forloop.parentloop.first and forloop.first and user.is_authenticated and task.task_type != 0 or task.can_be_unlocked %}
                                <li class="current" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span></span>
                                        <p attr-a="" attr-b="未解锁" color-a="green" color-b=""
                            {% else %}
                                <li class="lock" id="{{ task.task_rid }}" trace_task_index="{{ task.task_real_index }}" trace_task_name="{{ task.task_name }}">
                                    <div><span></span>
                                        <p attr-a="" attr-b="未解锁" color-a="green" color-b=""
                            {% endif %}
                                   desc="{{ task.task_desc }}"
                                   task_type="{{ task.task_type }}">{{ task.task_name }}</p></div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    {% endfor %}
"""
CURRENT_TASK = """
    {% if is_normal_class and current_task %}
        <div class="last-time">
            <h2 class="pos-l"><span>上次学习到</span>{{ current_task.task_name }}</h2>
            <a class="pos-r continue" rid="{{ current_task.task_rid }}">继续学习</a>
        </div>
    {% endif %}
"""