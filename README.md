# RedRabbit
自动批量关注某个b站up主的关注列表，前提是他开启了查看权限，最多能看到他100个关注的人

v1.0:
最基本功能。运行脚本后扫码登录b站，输入要copy的up主名字，回车运行

v1.1
小修改了扫码登录的等待逻辑，用法没变。
运行前修改command = ["taskkill", "/IM", "360AlbumViewer64.exe", "/F"] 列表里的360AlbumViewer64.exe为你自己的看图软件进程名。
不知道的话cmd中tasklist查一下
