# 任务清单

给view增加缓存操作
增加默认的创建超级管理员脚本
考虑重构BaseView功能，去掉猴子修复，优化工厂方法
完善自动注册路由功能，最好能够写一个数据库依赖，这样自动注册的路由不需要自己写数据库的连接。
优化页面访问，确认是否被访问了两次

注意：价格计算需要引入精确计算，防止计算误差问题

需要完成一些指定的特殊验证

需要做一些单独的设置，把view拆分开来，要求可以单独按照字段、methods来注册设备。

1、 增加针对不同method的生成schema
2、view改为组装方式，
3、注意修改depends的传递方式
4、 注意，post和put要返回规定值


当前任务：
实现delete
user接口重写

注意：重构的时候一定要区别model的server_default和default的区别，前者是不能调用的。
