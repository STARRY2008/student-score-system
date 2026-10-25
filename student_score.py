#  学生成绩查询系统
import json
import os
import tkinter as tk
from tkinter import messagebox
import datetime

DATA_FILE = "student_score.json"
#   加载初始数据函数
def load_data():
    if not os.path.exists(DATA_FILE):
        empty_data = {}
        with open(DATA_FILE,"w",encoding="utf-8") as f:
            json.dump(empty_data,f,ensure_ascii=False,indent=2)
            return empty_data
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        return json.load(f)
#   保存数据函数
def save_data(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
#   显示登录窗口
def show_login():
    login_win = tk.Tk()
    login_win.title("学生成绩查询系统-登录")
    login_win.geometry("400x400+500+300")
#   标题
    tk.Label(login_win, text="登录账号", font=("Arial", 20)).pack(pady=20)
#   输入账号
    tk.Label(login_win, text="账号").pack()
    entry_user = tk.Entry(login_win,font=("宋体",14))
    entry_user.pack(pady=5)
#  输入密码
    tk.Label(login_win, text="密码").pack()
    entry_pwd = tk.Entry(login_win,font=("宋体",14))
    entry_pwd.pack(pady=5)
#   登录按钮
    def on_login():
        data = load_data()
        username = entry_user.get()
        password = entry_pwd.get()
        if username not in data:
            messagebox.showerror("错误","该账号不存在")
            return
        if data[username]["pwd"] != password:
            messagebox.showerror("错误","密码错误")
            return
        messagebox.showinfo("登录成功","登录成功")
        role = data[username]["role"]
        login_win.destroy()
        if role == "student":
            show_student(username)
        else:
            show_teacher(username)
    tk.Button(login_win,text="登录",width=10,command=on_login).pack(pady=10)
#   注册按钮
    def on_register():
        login_win.destroy()
        show_account()
    tk.Button(login_win,text="注册",width=10,command=on_register).pack(pady=10)
    login_win.mainloop()
#   选择身份:学生/老师
def show_account():
    acc_win = tk.Tk()
    acc_win.title("学生成绩查询系统-选择身份")
    acc_win.geometry("400x400+500+300")
    tk.Label(acc_win,text="请选择身份",font="Arial").pack(pady=20)
    def choose_student():
        acc_win.destroy()
        show_register("student")
    def choose_teacher():
        acc_win.destroy()
        show_register("teacher")
    tk.Button(acc_win, text="学生",width=10,command=choose_student).pack(pady=5)
    tk.Button(acc_win, text="老师",width=10,command=choose_teacher).pack(pady=5)
    acc_win.mainloop()
#   显示注册窗口
def show_register(role):
    reg_win = tk.Tk()
    reg_win.title("学生成绩查询系统-注册")
    reg_win.geometry("400x400+500+300")
#   标题
    tk.Label(reg_win,text="注册账号", font=("Arial", 20)).pack(pady=20)
#   输入账号
    tk.Label(reg_win, text="账号").pack()
    entry_user = tk.Entry(reg_win, font=("宋体", 14))
    entry_user.pack(pady=5)
#   输入密码
    tk.Label(reg_win, text="密码").pack()
    entry_pwd = tk.Entry(reg_win, font=("宋体", 14))
    entry_pwd.pack(pady=5)
#   输入姓名
    tk.Label(reg_win, text="姓名").pack()
    entry_name = tk.Entry(reg_win, font=("宋体", 14))
    entry_name.pack(pady=5)
#   提交按钮
    def on_submit():
       data = load_data()
       username = entry_user.get()
       password = entry_pwd.get()
       name = entry_name.get()
       if not username or not password or not name:
           messagebox.showerror("错误!","账号、密码、姓名不能为空")
           return
       if username in data:
           messagebox.showerror("错误","账号已存在")
           return
       if role == "student":
            data[username] = {"pwd":password,"name":name,"role":"student","scores":[]}
       else:
            data[username] = {"pwd":password,"name":name,"role":"teacher"}
       save_data(data)
       messagebox.showinfo("成功","注册成功")
       reg_win.destroy()
       show_login()
    tk.Button(reg_win, text="提交", width=10, command=on_submit).pack(pady=10)
    reg_win.mainloop()
#   显示学生窗口菜单
def show_student(username):
    student_win = tk.Tk()
    student_win.title("学生成绩查询系统-学生菜单")
    student_win.geometry("400x400+500+300")
    data = load_data()
    name = data[username]["name"]
    #   标题
    tk.Label(student_win, text=f"{name}", font=("Arial", 20)).pack(pady=20)
#   查看成绩
    def view_scores():
        scores = data[username]["scores"]
        if not scores:
            messagebox.showerror("抱歉","您暂无成绩")
            return
        text =""
        for item in scores:
            text += f"{item['subject']},分数: {item['score']},日期: {item['date']}\n"
        messagebox.showinfo("我的成绩",text)
#   分析成绩
    def view_analysis():
        scores = data[username]["scores"]
        if not scores:
            messagebox.showerror("抱歉","暂无成绩,无法分析")
            return
        all_scores = [item['score'] for item in scores]
        avg = sum(all_scores) / len(all_scores)
        messagebox.showinfo("成绩分析",f"平均分: {avg:.2f}\n最高分: {max(all_scores)}\n最低分: {min(all_scores)}")
#   退出登录
    def logout():
        student_win.destroy()
        show_login()
    tk.Button(student_win,text="查看成绩",width=10,command=view_scores).pack(pady=10)
    tk.Button(student_win, text="成绩分析", width=10, command=view_analysis).pack(pady=10)
    tk.Button(student_win, text="退出登录", width=10, command=logout).pack(pady=10)
    student_win.mainloop()

#   显示教师窗口菜单
def show_teacher(username):
    teacher_win = tk.Tk()
    teacher_win.title("学生成绩查询系统-老师菜单")
    teacher_win.geometry("400x400+500+300")
    data = load_data()
    name = data[username]["name"]
    #   标题
    tk.Label(teacher_win, text=f"{name}", font=("Arial", 20)).pack(pady=20)
#   查看所有学生
    def view_all():
        text=""
        for uid,info in data.items():
            if info["role"] == "student":
                text += f"{uid} {info['name']}\n"
        messagebox.showinfo("所有学生",text if text else "暂无学生")
#   录入成绩
    def add_score():
        add_win = tk.Toplevel(teacher_win)
        add_win.title("录入成绩")
        add_win.geometry("400x400+500+300")
        tk.Label(add_win,text="学号").pack(pady=5)
        e_user = tk.Entry(add_win)
        e_user.pack()

        tk.Label(add_win,text="科目").pack(pady=5)
        e_subject = tk.Entry(add_win)
        e_subject.pack()

        tk.Label(add_win, text="分数").pack(pady=5)
        e_score = tk.Entry(add_win)
        e_score.pack()

        tk.Label(add_win, text="日期（YYYY-MM-DD,留空默认今天）").pack(pady=5)
        e_date = tk.Entry(add_win)
        e_date.pack()

#   显示提交按钮
        def submit():
            data = load_data()
            sid = e_user.get()
            subject = e_subject.get()
            score = e_score.get()
            date = e_date.get()

            if not sid or not subject or not score:
                messagebox.showerror("错误","成绩,科目,分数不能为空")
                return
            if sid not in data or data[sid]["role"] != "student":
                messagebox.showerror("错误","学号不存在或不是学生")
                return
            if not date:
                date = str(datetime.date.today())
            data[sid]["scores"].append({
                "subject":subject,
                "score":int(score),
                "date":date
            })
            save_data(data)
            messagebox.showinfo("成功","成绩已录入")
            add_win.destroy()
        tk.Button(add_win,text="提交",width=10,command=submit).pack(pady=10)
#   退出登录
    def logout():
        teacher_win.destroy()
        show_login()
    tk.Button(teacher_win,text="查看所有学生",width=10,command=view_all).pack(pady=10)
    tk.Button(teacher_win, text="录入成绩", width=10, command=add_score).pack(pady=10)
    tk.Button(teacher_win, text="退出登录", width=10, command=logout).pack(pady=10)
    teacher_win.mainloop()

if __name__ == "__main__":
    show_login()