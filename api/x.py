import httpx
import time

# response = httpx.get(
#     "http://qiyegpt.zhiy.cc/console/api/account/profile",
#     headers={
#         "Cookie": "_ga_DM9497FN4V=GS1.1.1694620108.8.1.1694620444.59.0.0; _ga=GA1.1.1911197445.1693239827; session=0126ca16-14cd-475a-ab7d-34dc07b9901a.LiqYZdc6qCyBKS_WwxNxYbtpOKo; _ga_2MFWXK7WYT=GS1.1.1694510544.5.0.1694510544.0.0.0; locale=zh-Hans; remember_token=d270758f-0760-4075-9a9c-3508e12dfc0f|c4fb2f8936c263c879baac8975f8e27361783ae5727373ec8e72446d6a89dea5b15d82aa89ac3afb73d28b0af0f029664685025dbb41cbf6e1db5c4eca6d3d1b"
#     },
# )

# print(response.text)

file = open("./y.txt", mode="r", encoding="utf-8")

for email in file.readlines()[880:]:
    email = email.replace("\n", "")
    print(email)

    response = httpx.post(
        "http://qiyegpt.zhiy.cc/console/api/workspaces/current/members/invite-email",
        json={
            "email": email,
            "role": "normal",
        },
        headers={
            "Cookie": "_ga_DM9497FN4V=GS1.1.1694623934.9.1.1694628145.48.0.0; _ga=GA1.1.1911197445.1693239827; session=0126ca16-14cd-475a-ab7d-34dc07b9901a.LiqYZdc6qCyBKS_WwxNxYbtpOKo; _ga_2MFWXK7WYT=GS1.1.1694510544.5.0.1694510544.0.0.0; locale=zh-Hans; remember_token=d270758f-0760-4075-9a9c-3508e12dfc0f|c4fb2f8936c263c879baac8975f8e27361783ae5727373ec8e72446d6a89dea5b15d82aa89ac3afb73d28b0af0f029664685025dbb41cbf6e1db5c4eca6d3d1b",
        },
    )
    time.sleep(1)

    print(response.text)

    response = httpx.post(
        "http://qiyegpt.zhiy.cc/console/api/setup",
        json={
            "email": email,
            "name": email.split('@')[0],
            "password": 'mhias303030',
        },
    )

    print(response.text)
