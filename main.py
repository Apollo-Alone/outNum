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
            demo2 = master.execute(1, cst.READ_HOLDING_REGISTERS, t, t1)
            # print(demo2)
            a = demo2[10]
            b = demo2[11]
            c = demo2[49]
            if c == 0:
                break
            result = ReadFloat((b, a))
        print(list)
    except modbus_tk.modbus.ModbusError as e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
