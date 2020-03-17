<br/>
<br/>

###爬取b站视频信息spider
<br/>  


>爬取的是视频的av号，分享数，点赞数，投币数，播放数。。。。以及弹幕内容

### 核心代码  

```python
    except:
        print('error')
        info = {'视频id': id, '最新弹幕数量': '', '金币数量': '', '不喜欢': '', '收藏': '', '最高排名': '', '点赞数': '', '目前排名': '', '回复数': '',
                '分享数': '', '观看数': ''}
        return info
    else:

        cid = content['data']['cid']
        title = content['data']['title']
        danmuku = get_danMuKu(cid)

        desp = content['data']["desc"]
        danmu = content['data']['stat']['danmaku']
        coin = content['data']['stat']['coin']
        dislike = content['data']['stat']['dislike']
        favorite = content['data']['stat']['favorite']
        his_rank = content['data']['stat']['his_rank']
        like = content['data']['stat']['like']
        now_rank = content['data']['stat']['now_rank']
        reply = content['data']['stat']['reply']
        share = content['data']['stat']['share']
        view = content['data']['stat']['view']```




#####请严格坚守robot.txt协议