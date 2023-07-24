import re

# 用于存储解析结果的数据结构
class Event:
    def __init__(self, event_type, time, node_id, device_id, message_type):
        self.event_type = event_type
        self.time = time
        self.node_id = node_id
        self.device_id = device_id
        self.message_type = message_type

# 解析单行文本的函数
def parse_line(line):
    # 提取事件类型、时间、节点ID、设备ID和消息类型
    event_type = line[0]
    time = float(re.search(r'\s(\d+\.\d+)\s', line).group(1))
    node_id = int(re.search(r'/NodeList/(\d+)', line).group(1))
    device_id = int(re.search(r'/DeviceList/(\d+)', line).group(1))

    adov_type = re.search(r'ns3::aodv::TypeHeader \((\w+)\)', line)
    message_type = None
    if adov_type != None:
        message_type = adov_type.group(1)
        print(adov_type)
    # 创建并返回事件对象
    return Event(event_type, time, node_id, device_id, message_type)

# 主函数，从文件中读取并解析数据
def main():
    events = []  # 用于存储所有事件的列表
    with open('small.tr', 'r') as file:  # 替换为你的文件名
        for line in file:
            event = parse_line(line)
            events.append(event)
    
    # 打印事件的概要信息
    for event in events:
        print(f'Event type: {event.event_type}, Time: {event.time}, Node ID: {event.node_id}, Device ID: {event.device_id}, Message type: {event.message_type}')

# 运行主函数
if __name__ == "__main__":
    main()
