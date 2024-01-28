import asyncio
import requests

async def mintNFT(name, description, imageUrl):

    imageUrl = "https://m.economictimes.com/thumb/msid-93499274,width-1600,height-900,resizemode-4,imgsize-99638/how-investible-are-nfts.jpg"
    url = "https://api.verbwire.com/v1/nft/mint/quickMintFromMetadata"

    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"chain\"\r\n\r\ngoerli\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n{name}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"description\"\r\n\r\n{description}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"imageUrl\"\r\n\r\n{imageUrl}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n{imageUrl}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"recipientAddress\"\r\n\r\n0x0E5d299236647563649526cfa25c39d6848101f5\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {
        "accept": "application/json",
        "content-type": "multipart/form-data; boundary=---011000010111000001101001",
        "X-API-Key": "sk_live_5b963604-629c-4156-ac69-433d1db6f108"
    }


    print("Minting your personal Nostalgia NFT")

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)

    print("Mint success!")

    return response.text


"""
name = input("Name: ")
description = input("Description: ")
imageUrl = input("Image Url: ")
asyncio.run(mintNFT(name, description, imageUrl))
"""