import struct

def extract_uvc_h264_data_packet(file):
    with open(file, "rb") as f:
        while True:
            # Read the first 12 bytes to get the packet length
            packet_header = f.read(12)
            if len(packet_header) == 0:
                # End of file
                break
            # Unpack the packet header to get the packet length
            packet_length = struct.unpack("<L", packet_header[8:12])[0]
            # Read the rest of the packet
            packet = f.read(packet_length - 12)
            # Check if this is a UVC H.264 data packet
            if packet[0] == 0x0E and packet[1] == 0x00:
                # Extract the H.264 data and save it to a new file
                h264_data = packet[12:]
                with open("h264_data.h264", "ab") as g:
                    g.write(h264_data)
            # Move to the next packet
            f.seek(packet_length, 1)
    print("UVC H.264 data packets extracted and saved to h264_data.h264")

extract_uvc_h264_data_packet("./7236_h264_uvc_0209.upv")
