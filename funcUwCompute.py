import time
import numpy as np
import collections

from cCommonGame import ShipType
from cCommonGame import ShipInfo
from cCommonGame import Position
from cCommonGame import UwCollectedData
from cCommonGame import UwParams


def uw_compute(uw_data):
    
    print("uw_data:")
    if isinstance(uw_data, collections.Iterable):
        for data in uw_data:
            print(data)
    else:
        print(uw_data)
        
    UwP = UwParams()
    
    outp = list()
	
    for i in range(len(uw_data)):
        # Generate background noise
        
        noise = np.random.randn(UwP.vector_len)
        
		# Check N
        for j in range(len(uw_data[i].N)):            
            # Check type and size
            ShipType = uw_data[i].N[j].ship_type
            ShipSize = uw_data[i].N[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
        
        outp.append(noise.tolist())
            
        # Check NE  
        for j in range(len(uw_data[i].NE)):            
            # Check type and size
            ShipType = uw_data[i].NE[j].ship_type
            ShipSize = uw_data[i].NE[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
         # Check E  
        for j in range(len(uw_data[i].E)):            
            # Check type and size
            ShipType = uw_data[i].E[j].ship_type
            ShipSize = uw_data[i].E[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
         # Check SE  
        for j in range(len(uw_data[i].SE)):            
            # Check type and size
            ShipType = uw_data[i].SE[j].ship_type
            ShipSize = uw_data[i].SE[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
         # Check S  
        for j in range(len(uw_data[i].S)):            
            # Check type and size
            ShipType = uw_data[i].S[j].ship_type
            ShipSize = uw_data[i].S[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
         # Check SW  
        for j in range(len(uw_data[i].SW)):            
            # Check type and size
            ShipType = uw_data[i].SW[j].ship_type
            ShipSize = uw_data[i].SW[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
         # Check W  
        for j in range(len(uw_data[i].W)):            
            # Check type and size
            ShipType = uw_data[i].W[j].ship_type
            ShipSize = uw_data[i].W[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
         # Check NW  
        for j in range(len(uw_data[i].NW)):            
            # Check type and size
            ShipType = uw_data[i].NW[j].ship_type
            ShipSize = uw_data[i].NW[j].size
            
            # Generate ship noise
            shipnoise = generate_shipnoise(ShipType,ShipSize,UwP)
            
            # Add ship noise to background noise
            noise = noise + shipnoise
            
        outp.append(noise.tolist())
        
    return outp
	
def obtain_params(ShipType,ShipSize,UwP):
    # Obtain sr and br
    if ShipType==0:
        # Military
        sr = UwP.mil_sr[ShipSize-1]
        br = UwP.mil_br[ShipSize-1]
    else:
        sr = UwP.civ_sr[ShipSize-1]
        br = UwP.civ_br[ShipSize-1]
    return sr,br
	
def generate_shipnoise(ShipType,ShipSize,UwP):
    shipnoise = np.zeros(UwP.vector_len)
    # Obtain params
    sr,br = obtain_params(ShipType,ShipSize,UwP)
    # Init shaft rate value and blade rate value
    SNR = random_range(UwP.SNR)
    SNR_br = SNR - random_range(UwP.SNR_br)
    freq = sr
    count = 1
    count_br = 1
    # Create all lines
    while freq<UwP.vector_len:
        if count>1:
            if np.mod(count,br)==0:
                # If its the blade rate
                if count_br>1:
                    #If its the harmonic
                    SNR_br = SNR_br-random_range(UwP.SNR_decay)
                SNR_value=SNR_br
                count_br=count_br+1
            else:
                SNR = SNR-random_range(UwP.SNR_decay)
                SNR_value = SNR
        else:
            SNR_value=SNR
        if np.random.rand(1)<UwP.p_ml:
            # probability of missing lines
            SNR_value=0
        if SNR_value<0:
            break
        shipnoise[freq-1]=SNR_value
        freq=freq+sr
        count=count+1
    
    return shipnoise
	
def random_range(input):
    # Produces a number that lies within the range defined by input
    outp = (input[1]-input[0])*np.random.rand(1)+input[0]
    return outp
	
#
if __name__ == '__main__':
    print("*** %s (%s)" % (__file__, time.ctime(time.time())))

    print("Test u/w ops")
    print("Sample data")
    collected_uw_data = list()
    collected_uw_data.append(UwCollectedData(N=[ShipInfo(ship_id=0,
                                                         ship_type=ShipType.MIL,
                                                         position=Position(0,0),
                                                         heading=0,
                                                         size=3,
                                                         is_sunken=False),
                                                ShipInfo(ship_id=1,
                                                         ship_type=ShipType.CIV,
                                                         position=Position(1, 2),
                                                         heading=180,
                                                         size=3,
                                                         is_sunken=False)]))
    collected_uw_data.append(UwCollectedData())
    collected_uw_data.append(UwCollectedData(E=[ShipInfo(ship_id=0,
                                                         ship_type=ShipType.MIL,
                                                         position=Position(0,0),
                                                         heading=0,
                                                         size=3,
                                                         is_sunken=False),
                                                ShipInfo(ship_id=1,
                                                         ship_type=ShipType.CIV,
                                                         position=Position(1, 2),
                                                         heading=180,
                                                         size=3,
                                                         is_sunken=False)]))
    collected_uw_data.append(UwCollectedData())
    collected_uw_data.append(UwCollectedData(S=[ShipInfo(ship_id=0,
                                                         ship_type=ShipType.MIL,
                                                         position=Position(0,0),
                                                         heading=0,
                                                         size=3,
                                                         is_sunken=False),
                                                ShipInfo(ship_id=1,
                                                         ship_type=ShipType.CIV,
                                                         position=Position(1, 2),
                                                         heading=180,
                                                         size=3,
                                                         is_sunken=False)]))

    # Perform computation
    outp = uw_compute(collected_uw_data)
    print("output:")
    if isinstance(outp, collections.Iterable):
        for data in outp:
            print(data)
    else:
        print(outp)

    print("*** END (%s)" % time.ctime(time.time()))