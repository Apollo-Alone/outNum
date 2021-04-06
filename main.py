import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct

logger = modbus_tk.utils.create_logger("console")


def ReadFloat(*args, reverse=False):
    for n, m in args:
        n, m = '%04x' % n, '%04x' % m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f', y_bytes)[0]
    y = round(y, 6)
    return y


if __name__ == "__main__":
    try:
        # 连接MODBUS TCP从机
        master = modbus_tcp.TcpMaster("192.168.20.133")
        master.set_timeout(5.0)
        logger.info("connected")
        t = 1
        t1 = 50
        for i in range(2):
            # @slave=1 : identifier of the slave. from 1 to 247.  0为广播所有的slave
            # @function_code=READ_HOLDING_REGISTERS：功能码
            # @starting_address=1：开始地址
            # @quantity_of_x=3：寄存器/线圈的数量
            # @output_value：一个整数或可迭代的值：1/[1,1,1,0,0,1]/xrange(12)
            # @data_format
            # @expected_length
            demo2 = master.execute(1, cst.READ_HOLDING_REGISTERS, t, t1)
            # 读保持寄存器
            logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 16))
            # 读输入寄存器
            logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 0, 16))
            # 读线圈寄存器
            logger.info(master.execute(1, cst.READ_COILS, 0, 16))
            # 读离散输入寄存器
            logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 16))
            # 单个读写寄存器操作
            # 写寄存器地址为0的保持寄存器
            logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, output_value=21))
            logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1))
            # 写寄存器地址为0的线圈寄存器，写入内容为0（位操作）
            logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 0, output_value=0))
            logger.info(master.execute(1, cst.READ_COILS, 0, 1))
            # 多个寄存器读写操作
            # 写寄存器起始地址为0的保持寄存器，操作寄存器个数为4
            logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[20, 21, 22, 23]))
            logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))
            # 写寄存器起始地址为0的线圈寄存器
            logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[0, 0, 0, 0]))
            logger.info(master.execute(1, cst.READ_COILS, 0, 4))
            a = demo2[10]
            b = demo2[11]
            c = demo2[49]
            if c == 0:
                break
            result = ReadFloat((b, a))
        print(list)
    except modbus_tk.modbus.ModbusError as e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
