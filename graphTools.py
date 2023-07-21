import config


def remove_isolated_nodes(adj_matrix):
    # 计算矩阵的行数和列数
    rows = len(adj_matrix)
    cols = len(adj_matrix[0])

    # 存储所有非孤立点的索引
    valid_nodes = set()

    # 遍历矩阵，找到所有非孤立点的索引
    for i in range(rows):
        for j in range(cols):
            if adj_matrix[i][j] == 1:
                valid_nodes.add(i)
                valid_nodes.add(j)

    # 对邻接矩阵进行切片，只保留有效节点的行和列
    new_matrix = [[adj_matrix[i][j] for j in range(
        cols) if j in valid_nodes] for i in range(rows) if i in valid_nodes]

    return new_matrix


def save_file(file_name, data, res_path=config.res_path):
    # 假设您有一个包含数据的List
    # 打开一个文件并将List的数据写入其中
    file_path = res_path + file_name
    with open(file_path, "w") as file:
        for item in data:
            file.write(str(item) + "\n")
