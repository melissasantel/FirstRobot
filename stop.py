import pypot.dynamixel


ports = pypot.dynamixel.get_available_ports()

if not ports:
    exit('no port')

global dxl_io
dxl_io = pypot.dynamixel.DxlIO(ports[0])


dxl_io.set_moving_speed({1:0,2:0})

