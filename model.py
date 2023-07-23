import math
from config import logger

# Constants
Pt = 4  # Transmit power in watts
Dt = 80e-3  # Transmit aperture diameter in meters
Dr = 80e-3  # Receive aperture diameter in meters
λ = 1500e-9  # Wavelength in meters
k = 1.38e-23  # Boltzmann constant in J/K
T = 34718969.08372476  # Noise temperature in K
B = 1.25e9  # Channel bandwidth in Hz
LightSpeed = 3e8  # Speed of light in m/s
Constant_latency_ms = 20

# for test
z = 1000e3  # Distance between transmitter and receiver in meters



def from_dis_to_cbps(dis_m):
    # Calculate received power Pr
    Pr = Pt * Dt**2 * math.pi**2 * Dr**2 / (16 * dis_m**2 * λ**2) * 0.9 * 0.9
    # Calculate received thermal noise power N
    N = k * T * B
    # Calculate SNR
    SNR = Pr / N
    # Calculate C
    C_bps = B * math.log2(1 + SNR)
    logger.debug(f"Distance: {dis_m}, Received power Pr: {Pr} W, noise power N: {N} W, SNR: {SNR}, C: {C_bps} bps")
    return int(C_bps)

def from_dis_to_latency(dis_m):
    latency_ms = dis_m / LightSpeed * 1000 + Constant_latency_ms
    logger.info(f"Distance: {dis_m}m , latency: {latency_ms}ms")
    return int(latency_ms)


if __name__ == "__main__":
    res1 = from_dis_to_cbps(5000e3)
    res2 = from_dis_to_cbps(2000e3)
    logger.info(f"res1:{res1}bps, res2:{res2}bps")