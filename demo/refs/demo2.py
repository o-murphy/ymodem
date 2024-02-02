import os
import time

from construct import *
from tqdm import tqdm

from ymodem.CRC import calc_crc16

# # C
# p0 = b'\x01\x00\xFF\x52\x69\x73\x63\x76\x5F\x46\x69\x72\x6D\x77\x61\x72\x65\x5F\x32\x33\x30\x39\x32\x31\x2E\x62\x69\x6E\x00\x34\x33\x30\x36\x38\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\xF4'
# # C
# p1 = b'\x02\x01\xFE\x97\xA1\x06\x00\x93\x81\x01\x9B\x17\xD1\x10\x00\x13\x01\x81\x9C\x17\xE5\x05\x00\x13\x05\xC5\x9A\x97\xE5\x05\x00\x93\x85\x45\x9A\x17\x96\x06\x00\x13\x06\xC6\x23\x63\xFC\xC5\x00\x83\x22\x05\x00\x23\xA0\x55\x00\x13\x05\x45\x00\x93\x85\x45\x00\xE3\xE8\xC5\xFE\x17\x95\x06\x00\x13\x05\xC5\x21\x97\xC5\x10\x00\x93\x85\x05\x98\x63\x78\xB5\x00\x23\x20\x05\x00\x13\x05\x45\x00\xE3\x6C\xB5\xFE\xEF\x00\x00\x15\xEF\x60\x81\x6C\x6F\x00\x00\x00\x67\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xB3\x67\xB5\x00\x93\xF7\x37\x00\x63\x92\x07\x08\x03\xA7\x05\x00\xB7\x86\x7F\x7F\x93\x86\xF6\xF7\xB3\x77\xD7\x00\xB3\x87\xD7\x00\xB3\xE7\xE7\x00\xB3\xE7\xD7\x00\x13\x06\xF0\xFF\x63\x9E\xC7\x06\x13\x06\x05\x00\x13\x08\xF0\xFF\x13\x06\x46\x00\x93\x85\x45\x00\x23\x2E\xE6\xFE\x03\xA7\x05\x00\xB3\x77\xD7\x00\xB3\x87\xD7\x00\xB3\xE7\xE7\x00\xB3\xE7\xD7\x00\xE3\x80\x07\xFF\x83\xC7\x05\x00\x03\xC7\x15\x00\x83\xC6\x25\x00\x23\x00\xF6\x00\x63\x8A\x07\x00\xA3\x00\xE6\x00\x63\x06\x07\x00\x23\x01\xD6\x00\x63\x94\x06\x00\x67\x80\x00\x00\xA3\x01\x06\x00\x67\x80\x00\x00\x93\x07\x05\x00\x03\xC7\x05\x00\x93\x87\x17\x00\x93\x85\x15\x00\xA3\x8F\xE7\xFE\xE3\x18\x07\xFE\x67\x80\x00\x00\x13\x06\x05\x00\x6F\xF0\x1F\xFB\x13\x01\x01\xFF\x23\x24\x81\x00\x23\x20\x21\x01\x17\xE4\x05\x00\x13\x04\x04\x80\x17\xD9\x05\x00\x13\x09\x89\x7F\x33\x09\x89\x40\x23\x26\x11\x00\x23\x22\x91\x00\x13\x59\x29\x40\x63\x0E\x09\x00\x93\x04\x00\x00\x83\x27\x04\x00\x93\x84\x14\x00\x13\x04\x44\x00\xE7\x80\x07\x00\xE3\x18\x99\xFE\x17\xD4\x05\x00\x13\x04\x44\x7C\x17\xD9\x05\x00\x13\x09\xC9\x7B\x33\x09\x89\x40\x13\x59\x29\x40\x63\x0E\x09\x00\x93\x04\x00\x00\x83\x27\x04\x00\x93\x84\x14\x00\x13\x04\x44\x00\xE7\x80\x07\x00\xE3\x18\x99\xFE\x83\x20\xC1\x00\x03\x24\x81\x00\x83\x24\x41\x00\x03\x29\x01\x00\x13\x01\x01\x01\x67\x80\x00\x00\xB3\xC7\xA5\x00\x93\xF7\x37\x00\xB3\x08\xC5\x00\x63\x92\x07\x06\x93\x07\x30\x00\x63\xFE\xC7\x04\x93\x77\x35\x00\x13\x07\x05\x00\x63\x98\x07\x06\x13\xF6\xC8\xFF\x93\x07\x06\xFE\x63\x6C\xF7\x08\x63\x7C\xC7\x02\x93\x86\x05\x00\x93\x07\x07\x00\x03\xA8\x06\x00\x93\x87\x47\x00\x93\x86\x46\x00\x23\xAE\x07\xFF\xE3\xE8\xC7\xFE\x93\x07\xF6\xFF\xB3\x87\xE7\x40\x93\xF7\xC7\xFF\x93\x87\x47\x00\x33\x07\xF7\x00\xB3\x85\xF5\x00\x63\x68\x17\x01\x67\x80\x00\x00\x13\x07\x05\x00\xE3\x7C\x15\xFF\x83\xC7\x05\x00\x13\x07\x17\x00\x93\x85\x15\x00\xA3\x0F\xF7\xFE\xE3\x68\x17\xFF\x67\x80\x00\x00\x83\xC6\x05\x00\x13\x07\x17\x00\x93\x77\x37\x00\xA3\x0F\xD7\xFE\x93\x85\x15\x00\xE3\x80\x07\xF8\x83\xC6\x05\x00\x13\x07\x17\x00\x93\x77\x37\x00\xA3\x0F\xD7\xFE\x93\x85\x15\x00\xE3\x9A\x07\xFC\x6F\xF0\x5F\xF6\x83\xA6\x05\x00\x83\xA2\x45\x00\x83\xAF\x85\x00\x03\xAF\xC5\x00\x83\xAE\x05\x01\x03\xAE\x45\x01\x03\xA3\x85\x01\x03\xA8\xC5\x01\x93\x85\x45\x02\x23\x20\xD7\x00\x83\xA6\xC5\xFF\x23\x22\x57\x00\x23\x24\xF7\x01\x23\x26\xE7\x01\x23\x28\xD7\x01\x23\x2A\xC7\x01\x23\x2C\x67\x00\x23\x2E\x07\x01\x13\x07\x47\x02\x23\x2E\xD7\xFE\xE3\x68\xF7\xFA\x6F\xF0\x9F\xF1\x13\x03\xF0\x00\x13\x07\x05\x00\x63\x7E\xC3\x02\x93\x77\xF7\x00\x63\x90\x07\x0A\x63\x92\x05\x08\x93\x76\x06\xFF\x13\x76\xF6\x00\xB3\x86\xE6\x00\x23\x20\xB7\x00\x23\x22\xB7\x00\x23\x24\xB7\x00\x23\x26\xB7\x00\x13\x07\x07\x01\xE3\x66\xD7\xFE\x63\x14\x06\x00\x67\x80\x00\x00\xB3\x06\xC3\x40\x93\x96\x26\x00\x97\x02\x00\x00\xB3\x86\x56\x00\x67\x80\xC6\x00\x23\x07\xB7\x00\xA3\x06\xB7\x00\x23\x06\xB7\x00\xA3\x05\xB7\x00\x23\x05\xB7\x00\xA3\x04\xB7\x00\x23\x04\xB7\x00\xA3\x03\xB7\x00\x23\x03\xB7\x00\xA3\x02\xB7\x00\x23\x02\xB7\x00\xA3\x01\xB7\x00\x23\x01\xB7\x00\xA3\x00\xB7\x00\x23\x00\xB7\x00\x67\x80\x00\x00\x93\xF5\xF5\x0F\x93\x96\x85\x00\x5B\xD8'
#
# #
# # ACK
# p2 = b'\x02\x02\xFD\xB3\xE5\xD5\x00\x93\x96\x05\x01\xB3\xE5\xD5\x00\x6F\xF0\xDF\xF6\x93\x96\x27\x00\x97\x02\x00\x00\xB3\x86\x56\x00\x93\x82\x00\x00\xE7\x80\x06\xFA\x93\x80\x02\x00\x93\x87\x07\xFF\x33\x07\xF7\x40\x33\x06\xF6\x00\xE3\x78\xC3\xF6\x6F\xF0\xDF\xF3\x13\x01\x01\xF6\x13\x0E\xC1\x08\x23\x2A\xF1\x08\x37\x03\x00\x80\xB7\x07\xFF\xFF\x93\x8E\x05\x00\x13\x43\xF3\xFF\x23\x26\xD1\x08\x93\x87\x87\x20\x93\x05\x81\x00\x93\x06\x0E\x00\x23\x2E\x11\x06\x23\x2A\xF1\x00\x23\x28\xE1\x08\x23\x2C\x01\x09\x23\x2E\x11\x09\x23\x24\xD1\x01\x23\x2C\xD1\x01\x23\x2E\x61\x00\x23\x28\x61\x00\x23\x22\xC1\x01\xEF\x00\x10\x18\x83\x27\x81\x00\x23\x80\x07\x00\x83\x20\xC1\x07\x13\x01\x01\x0A\x67\x80\x00\x00\x93\x0E\x05\x00\x13\x85\xC1\x86\x13\x01\x01\xF6\x03\x25\x05\x00\x13\x0E\x81\x08\x23\x2A\xF1\x08\x37\x03\x00\x80\xB7\x07\xFF\xFF\x13\x43\xF3\xFF\x23\x24\xC1\x08\x23\x26\xD1\x08\x93\x87\x87\x20\x13\x86\x05\x00\x93\x06\x0E\x00\x93\x05\x81\x00\x23\x2E\x11\x06\x23\x2A\xF1\x00\x23\x28\xE1\x08\x23\x2C\x01\x09\x23\x2E\x11\x09\x23\x24\xD1\x01\x23\x2C\xD1\x01\x23\x2E\x61\x00\x23\x28\x61\x00\x23\x22\xC1\x01\xEF\x00\x50\x10\x83\x27\x81\x00\x23\x80\x07\x00\x83\x20\xC1\x07\x13\x01\x01\x0A\x67\x80\x00\x00\x93\xF6\xF5\x0F\x93\x77\x35\x00\x63\x8C\x06\x0C\x63\x86\x07\x02\x83\x47\x05\x00\x63\x82\x07\x0C\x63\x9A\xF6\x00\x6F\x00\xC0\x14\x83\x47\x05\x00\x63\x8A\x07\x0A\x63\x8A\xD7\x0A\x13\x05\x15\x00\x93\x77\x35\x00\xE3\x96\x07\xFE\x93\xF5\xF5\x0F\x93\x97\x85\x00\xB3\xE5\xF5\x00\x03\x27\x05\x00\x13\x93\x05\x01\x33\x63\xB3\x00\x37\x08\xFF\xFE\x33\x46\xE3\x00\x13\x08\xF8\xEF\x93\x47\xF7\xFF\x93\x45\xF6\xFF\x33\x07\x07\x01\x33\x06\x06\x01\xB3\xF7\xE7\x00\x33\xF6\xC5\x00\xB7\x88\x80\x80\xB3\xE7\xC7\x00\x93\x88\x08\x08\xB3\xF7\x17\x01\x63\x9A\x07\x02\x13\x05\x45\x00\x03\x27\x05\x00\x33\x46\x67\x00\xB3\x07\x07\x01\xB3\x05\x06\x01\x13\x47\xF7\xFF\x13\x46\xF6\xFF\xB3\xF7\xE7\x00\x33\xF6\xC5\x00\xB3\xE7\xC7\x00\xB3\xF7\x17\x01\xE3\x8A\x07\xFC\x83\x47\x05\x00\x63\x8E\x07\x00\x63\x96\xF6\x00\x6F\x00\x80\x01\x63\x8C\xD7\x08\x13\x05\x15\x00\x83\x47\x05\x00\xE3\x9A\x07\xFE\x13\x05\x00\x00\x67\x80\x00\x00\x63\x82\x07\x02\x83\x47\x05\x00\x63\x98\x07\x00\x6F\x00\x80\x07\x83\x47\x05\x00\xE3\x84\x07\xFE\x13\x05\x15\x00\x93\x77\x35\x00\xE3\x98\x07\xFE\x03\x27\x05\x00\x37\x06\xFF\xFE\x13\x06\xF6\xEF\xB3\x07\xC7\x00\xB7\x86\x80\x80\x13\x47\xF7\xFF\xB3\xF7\xE7\x00\x93\x86\x06\x08\xB3\xF7\xD7\x00\x63\x90\x07\x02\x13\x05\x45\x00\x03\x27\x05\x00\xB3\x07\xC7\x00\x13\x47\xF7\xFF\xB3\xF7\xE7\x00\xB3\xF7\xD7\x00\xE3\x84\x07\xFE\x83\x47\x05\x00\xE3\x88\x07\xF8\x13\x05\x15\x00\x83\x47\x05\x00\xE3\x9C\x07\xFE\x67\x80\x00\x00\x67\x80\x00\x00\x67\x80\x00\x00\x67\x80\x00\x00\x93\x77\x35\x00\x13\x07\x05\x00\x63\x9C\x07\x04\xB7\x86\x7F\x7F\x93\x86\xF6\xF7\x93\x05\xF0\xFF\x13\x07\x47\x00\x03\x26\xC7\xFF\xB3\x77\xD6\x00\xB3\x87\xD7\x00\xB3\xE7\xC7\x00\xB3\xE7\xD7\x00\xE3\x84\xB7\xFE\x83\x46\xC7\xFF\xB3\x07\xA7\x40\x03\x46\xD7\xFF\x03\x45\xE7\xFF\x63\x80\x06\x04\x63\x0A\x06\x02\x33\x35\xA0\x00\x33\x05\xF5\x00\x13\x05\xE5\xFF\x67\x80\x00\x00\xE3\x88\x06\xFA\x83\x47\x07\x00\x13\x07\x17\x00\x93\x76\x37\x00\xE3\x98\x07\xFE\x33\x07\xA7\x40\x13\x05\xF7\xFF\x67\x80\x00\x00\x13\x85\xD7\xFF\x67\x80\x00\x00\x13\x85\xC7\xFF\x67\x80\x00\x00\x13\x01\x01\xBB\x23\x24\x81\x44\x23\x22\x91\x44\x23\x26\x71\x43\x23\x22\x91\x43\x23\x20\xA1\x43\x23\x2E\xB1\x41\x93\x04\x06\x00\x93\x8C\x06\x00\x23\x26\x11\x44\x23\x20\x21\x45\x23\x2E\x31\x43\x23\x2C\x41\x43\x23\x2A\x51\x43\x23\x28\x61\x43\x23\x24\x81\x43\x13\x04\x05\x00\x13\x8D\x05\x00\x93\x0B\x10\x00\x93\x06\x10\x00\x13\x06\x00\x00\x93\x0D\xF0\xFF\xB3\x87\xB4\x01\x33\x87\xD7\x00\xB3\x87\xC6\x00\xB3\x85\xF4\x00\x63\xF8\x97\x03\x83\xC5\x05\x00\x03\x47\x07\x00\x63\xF8\xE5\x1E\x13\x86\x07\x00\x93\x06\x10\x00\xB3\x8B\xB7\x41\xB3\x87\xB4\x01\x33\x87\xD7\x00\xB3\x87\xC6\x00\xB3\x85\xF4\x00\xE3\xEC\x97\xFD\x93\x08\x10\x00\x93\x06\x10\x00\x13\x06\x00\x00\x93\x05\xF0\xFF\xB3\x87\xB4\x00\x33\x87\xD7\x00\xB3\x87\xC6\x00\x33\x85\xF4\x00\x63\xF8\x97\x03\x03\x45\x05\x00\x03\x47\x07\x00\x63\x7C\xA7\x1A\x13\x86\x07\x00\x93\x06\x10\x00\xB3\x88\xB7\x40\xB3\x87\xB4\x00\x33\x87\xD7\x00\xB3\x87\xC6\x00\x33\x85\xF4\x00\xAC\x53'
# #
# # ACK
# p3 = b'\x02\x03\xFC\xE3\xEC\x97\xFD\x93\x85\x15\x00\x93\x8D\x1D\x00\x63\xE6\xB5\x01\x93\x8B\x08\x00\x93\x8D\x05\x00\x93\x07\x01\x01\x13\x07\x01\x41\x23\xA0\x97\x01\x93\x87\x47\x00\xE3\x1C\xF7\xFE\x13\x89\xFC\xFF\xB3\x85\x94\x01\x13\x87\x04\x00\x33\x86\x24\x01\x63\x82\x0C\x02\x83\x47\x07\x00\x13\x05\x01\x41\xB3\x06\xE6\x40\x93\x97\x27\x00\xB3\x07\xF5\x00\x13\x07\x17\x00\x23\xA0\xD7\xC0\xE3\x12\xB7\xFE\x13\x86\x0D\x00\xB3\x85\x74\x01\x13\x85\x04\x00\xEF\x60\x90\x21\x63\x1A\x05\x1A\x93\x8A\xFD\xFF\xB3\x07\x54\x01\xB7\x19\x00\x00\x23\x24\xF1\x00\x13\x0A\x10\x00\xB3\x87\x54\x01\x93\x89\x09\x80\x13\x0B\x00\x00\x13\x0C\x00\x00\x23\x26\xF1\x00\x33\x0A\xBA\x41\xB3\xE9\x3C\x01\x33\x06\x84\x01\xB3\x07\x26\x01\x83\xC7\x07\x00\x13\x07\x01\x41\x93\x97\x27\x00\xB3\x07\xF7\x00\x83\xA7\x07\xC0\x63\x8C\x07\x06\x63\x06\x0B\x00\x63\xF4\x77\x01\xB3\x87\x7C\x41\x33\x0C\xFC\x00\x13\x0B\x00\x00\xB3\x07\x9D\x41\xE3\xF4\x87\xFD\x33\x05\xA4\x01\x93\x85\x09\x00\xEF\x70\x90\x58\x33\x0D\xAD\x00\xB3\x07\x9D\x41\xE3\xF8\x87\xFB\x13\x05\x00\x00\x83\x20\xC1\x44\x03\x24\x81\x44\x83\x24\x41\x44\x03\x29\x01\x44\x83\x29\xC1\x43\x03\x2A\x81\x43\x83\x2A\x41\x43\x03\x2B\x01\x43\x83\x2B\xC1\x42\x03\x2C\x81\x42\x83\x2C\x41\x42\x03\x2D\x01\x42\x83\x2D\xC1\x41\x13\x01\x01\x45\x67\x80\x00\x00\x93\x07\x0B\x00\x63\x74\xBB\x01\x93\x87\x0D\x00\x63\xF6\x27\x07\xB3\x06\xF4\x00\xB3\x86\x86\x01\x33\x87\xF4\x00\x6F\x00\x80\x01\x93\x87\x17\x00\x33\x87\x87\x01\xB3\x86\xF4\x00\x33\x07\xE4\x00\x63\xF4\x27\x05\x83\xC6\x06\x00\x03\x47\x07\x00\xE3\x82\xE6\xFE\x33\x0C\x8A\x01\x6F\xF0\x5F\xF5\x63\x86\xE5\x08\x93\x0D\x06\x00\x93\x0B\x10\x00\x13\x06\x16\x00\x93\x06\x10\x00\x6F\xF0\x1F\xDE\x63\x00\xE5\x08\x93\x05\x06\x00\x93\x08\x10\x00\x13\x06\x16\x00\x93\x06\x10\x00\x6F\xF0\x9F\xE1\x93\x86\x0A\x00\x63\x70\xBB\x1D\x83\x27\x81\x00\xB3\x87\x87\x01\x03\xC7\x07\x00\x83\x27\xC1\x00\x83\xC7\x07\x00\x63\x0C\xF7\x00\x6F\x00\x40\x1A\x83\xC5\x05\x00\x83\xC7\x07\x00\x63\x9E\xF5\x00\x93\x06\x07\x00\x13\x87\xF6\xFF\xB3\x07\x87\x01\xB3\x85\xE4\x00\xB3\x07\xF4\x00\xE3\x10\xDB\xFE\x93\x08\x1B\x00\x63\xE2\x16\x19\x33\x0C\x7C\x01\x33\x8B\x7C\x41\x6F\xF0\x1F\xED\x63\x8E\x76\x15\x93\x86\x16\x00\x6F\xF0\x1F\xD6\x63\x82\x16\x15\x93\x86\x16\x00\x6F\xF0\x5F\xDA\xB3\x8B\xBC\x41\x63\xE6\xBB\x13\x93\x8A\xFD\xFF\xB7\x19\x00\x00\xB3\x87\x54\x01\x13\x0A\x10\x00\x93\x89\x09\x80\x93\x8B\x1B\x00\x13\x0C\x00\x00\x23\x24\xF1\x00\x13\x8B\xED\xFF\x33\x0A\xBA\x41\xB3\xE9\x3C\x01\xB3\x05\x84\x01\xB3\x87\x25\x01\x83\xC7\x07\x00\x13\x07\x01\x41\x93\x97\x27\x00\xB3\x07\xF7\x00\x83\xA7\x07\xC0\x63\x84\x07\x04\x33\x0C\xFC\x00\xB3\x07\x9D\x41\xE3\xFC\x87\xFD\x33\x05\xA4\x01\x93\x85\x09\x00\xEF\x70\x50\x3E\x33\x0D\xAD\x00\xB3\x07\x9D\x41\xE3\xE0\x87\xE7\xB3\x05\x84\x01\xB3\x87\x25\x01\x83\xC7\x07\x00\x13\x07\x01\x41\x93\x97\x27\x00\xB3\x07\xF7\x00\x83\xA7\x07\xC0\xE3\x90\x07\xFC\x63\xF0\x2D\x05\x33\x87\xB5\x01\xB3\x87\xB4\x01\x03\x46\x07\x00\x03\xC7\x07\x00\x93\x87\x0D\x00\x63\x0A\xE6\x00\x6F\x00\x00\x07\x03\x46\x06\x00\x03\x47\x07\x00\x63\x12\xE6\x06\x93\x87\x17\x00\x33\x07\xFC\x00\x33\x86\xF4\x00\x33\x07\xE4\x00\xE3\xE2\x27\xFF\x93\x07\xF0\xFF\x63\x84\xFA\x08\xB3\x87\x55\x01\x03\xC7\x07\x00\x83\x27\x81\x00\x83\xC7\x07\x00\x63\x16\xF7\x02\x33\x07\x6C\x01\xB3\x87\x64\x01\x33\x07\xE4\x00\x13\x88\xF4\xFF\x63\x80\x07\x07\x03\xC5\x07\x00\x03\x46\x07\x00\x93\x87\xF7\xFF\x13\x07\xF7\xFF\xE3\x06\xC5\xFE\x33\x0C\x7C\x01\x6F\xF0\x9F\xF3\xB3\x06\x8A\x01\x33\x8C\xF6\x00\x6F\xF0\xDF\xF2\x93\x8B\x0D\x00\x6F\xF0\x5F\xED\x13\x86\x07\x00\x93\x06\x10\x00\x6F\xF0\x1F\xC6\x13\x86\x07\x00\x93\x06\x10\x00\x6F\xF0\x5F\xC0\x93\x86\x0D\x00\x93\x08\x1B\x00\xE3\xF2\x16\xE9\x13\x05\x06\x00\x6F\xF0\x9F\xD7\x13\x85\x05\x00\x6F\xF0\x1F\xD7\x13\x01\x01\xFA\x23\x2C\x81\x04\x23\x2A\x91\x04\x23\x2E\x11\x04\x23\x28\x21\x05\x23\x26\x31\x05\x23\x24\x41\x05\x23\x22\x51\x05\x93\x84\x05\x00\x83\xC5\x05\x00\x13\x04\x05\x00\x63\x8C\x05\x0E\x83\xC6\x14\x00\x63\x84\x06\x1A\x03\xC6\x24\x00\x63\x08\x06\x10\x03\xC7\x34\x00\x63\x02\x07\x1A\x83\xC7\x44\x00\x63\x80\x07\x14\x13\x85\x04\x00\xEF\xF0\xDF\xAA\x13\x09\x05\x00\x93\x65\x05\x20\x13\x05\x04\x00\xEF\x70\xD0\x27\x63\x66\x25\x17\x93\x07\xE0\x0F\x3F\x28'
# #
# #


Control = Enum(
    Int8ul,
    C=0x43,
    ACK=0x06,
    CAN=0x18,
    CRC=0x43,
    EOT=0x04,
    G=0x67,
    NAK=0x15,
    SOH=0x01,
    STX=0x02
)

Packet = Struct(
    control=Control,
    seq_hi=Int8ul,
    seq_low=Checksum(Byte, lambda x: 0xff - x, lambda ctx: ctx.seq_hi),
    data=Bytes(lambda ctx: 128 if ctx.control == Control.SOH else 1024),
    crc=Checksum(Bytes(2), lambda data: calc_crc16(data).to_bytes(2, 'little'), lambda ctx: ctx.data),
)

TransactionHeader = Struct(
    filename=CString('utf8'),
    size_=CString('utf8'),
    # size=Computed(lambda ctx: int(ctx.size_))
)


# d = Packet.parse(p1)
# print(len(p1))
# print(d)
# # print(d.data)
#
# # d1 = Packet.parse(p1)
# # print(d1)
# #
# # d2 = Packet.parse(p2)
# # print(d2)
# #
# # d3 = Packet.parse(p3)
# # print(d3)
#
# pp = Packet.build(dict(control=Control.STX, seq_hi=1, data=d.data))
# # print(p1)
# #
# # print(pp)
# print(Packet.parse(pp))


class YReceiver:
    def __init__(self):
        self._filename = None
        self._size = None
        self._eot = False
        self._data = b''

        # self._r = Control.CRC

    @property
    def data(self):
        return self._data

    def receiver_emulator(self, packet: [bytes, bytearray]) -> [bytes, bytearray]:

        if packet == b'':
            return Control.build(Control.CRC)

        try:
            ctrl = Control.parse(packet)
            print(ctrl)
        except Exception as exc:
            print(exc)
            return Control.build(Control.CAN)

        if ctrl == Control.CAN:
            ret = Control.CRC

        elif ctrl == Control.EOT:
            if not self._eot:
                self._eot += True
                ret = Control.NAK
            else:
                ret = Control.ACK

        else:
            try:
                parsed = Packet.parse(packet)
            except Exception as exc:
                print(exc)
                return Control.build(Control.CRC)

            if ctrl == Control.SOH and parsed.seq_hi == 0:
                header = TransactionHeader.parse(parsed.data)
                self._filename = header.filename
                self._size = header.size_
                ret = Control.ACK

            elif ctrl == Control.SOH or ctrl == Control.STX:
                self._data += parsed.data
                ret = Control.ACK

            else:
                ret = Control.CAN

        return Control.build(ret)


class YSender:

    @staticmethod
    def create_data_packet(data, seq, header=False):

        if header:
            return Packet.build(
                dict(
                    control=Control.SOH,
                    seq_hi=0,
                    data=data
                )
            )

        if len(data) < 1024:
            data += b'\x00' * (1024 - len(data))

        return Packet.build(
            dict(
                control=Control.STX,
                seq_hi=seq,
                data=data
            )
        )

    @staticmethod
    def send_file(filepath, request, timeout=0.01):

        if not callable(request):
            raise Exception("request have to be callable")

        def _request(packet):
            return Control.parse(request(packet))

        # # Inspecting the function
        # signature = inspect.signature(request)
        # parameters = signature.parameters
        # return_type = get_type_hints(request).get('return', None)

        # Send header packet with filename and size
        filename = filepath.split('/')[-1].encode()
        filesize = os.path.getsize(filepath)
        size = str(filesize).encode()

        header_data = filename + b'\x00' + size + b'\x00'
        padding = b'\x00' * (128 - len(header_data))
        header_data += padding

        # transaction = YReceiver()

        header_packet = YSender.create_data_packet(header_data, 0, True)
        # resp = transaction.request(header_packet)
        resp = _request(header_packet)

        if resp != Control.CRC:
            raise Exception("Wrong header")

        bar = tqdm(
            total=filesize,
            unit_divisor=1024,
            unit_scale=True,
            unit='b',
            # bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
            colour="green"
        )

        with open(filepath, 'rb') as fp:
            seq = 1
            while data := fp.read(1024):
                data_packet = YSender.create_data_packet(data, seq)

                # resp = transaction.request(data_packet)
                resp = _request(data_packet)
                print(seq, resp)

                if not resp in [Control.ACK, Control.CRC]:
                    bar.colour = 'red'
                    raise Exception("Error, not ACK received")

                bar.update(len(data))

                time.sleep(timeout)

                seq += 1
                if seq > 255:
                    seq = 0

            # EOT
            # resp = transaction.request(Control.build(Control.EOT))
            resp = _request(Control.build(Control.EOT))
            if resp != Control.NAK:
                bar.colour = 'red'
                raise Exception("Invalid EOT, not NAK received")

            # EOT
            # resp = transaction.request(Control.build(Control.EOT))
            resp = _request(Control.build(Control.EOT))
            if resp != Control.ACK:
                bar.colour = 'red'
                raise Exception("Invalid EOT, not ACK received")

            bar.colour = 'magenta'


# def create_header_packet(file_path):
#     # Send header packet with filename and size
#     filename = file_path.split('/')[-1].encode()
#     filesize = os.path.getsize(file_path)
#     size = str(filesize).encode()
#     header_data = filename + b'\x00' + size + b'\x00'
#
#     return Packet.build(
#         dict(
#             control=Control.SOH,
#             seq_hi=0,
#             data=header_data + b'\x00' * (128 - len(header_data))
#         )
#     )


import serial


def receive(ser):
    r = YReceiver()

    buf = b''

    while True:
        bytesToRead = ser.inWaiting()
        data = ser.read(bytesToRead)

        _EOT = True

        if bytesToRead > 0:
            _EOT = False
            buf += data

        else:

            if len(buf) > 0:
                # print(buf)
                resp = r.receiver_emulator(buf)
                print(resp)
                ser.write(resp)

                if r._eot:
                    _EOT = True
                    with open('dump.bin', 'wb') as fp:
                        fp.write(r.data)

                buf = b''

            else:

                if _EOT:
                    time.sleep(0.2)
                    print('C')
                    ser.write(b'C')


def example():
    filepath = 'demo/local/sample6.bin'

    YSender.send_file(
        filepath,
        YReceiver().receiver_emulator
    )


def serial_send(data, ser):
    count = ser.write(data)
    if count > 0:
        response = ser.read()
        return response



ser = serial.Serial(port='COM5', baudrate=115200,
                    bytesize=8, parity='N', stopbits=1, timeout=10, xonxoff=False, rtscts=False)
try:

    # receive(ser)






    filepath = 'demo/local/sample6.bin'
    YSender.send_file(
        filepath=filepath,
        request=lambda data: serial_send(data, ser)
    )
except Exception as ex:
    print(ex)

if ser.is_open():
    ser.close()