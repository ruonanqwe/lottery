from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__)

class LotteryState:
    def __init__(self):
        self.is_active = False
        self.numbers = []  # 所有可用号码
        self.drawn_numbers = {}  # 已抽取的号码 {ip: {'number': number, 'time': datetime}}
        self.used_numbers = set()  # 已使用的号码集合，用于快速查重
        self.reset()
    
    def reset(self):
        """重置抽奖系统，生成号码库"""
        # 生成6位数号码库
        self.numbers = [f"{i:06d}" for i in range(1, 1000000)]  # 生成所有6位数
        random.shuffle(self.numbers)  # 随机打乱顺序
        self.drawn_numbers.clear()
        self.used_numbers.clear()
    
    def draw(self, ip):
        """从号码库中抽取号码"""
        if not self.is_active:
            return None, "抽奖活动尚未开始或已经结束！"
        
        if ip in self.drawn_numbers:
            return None, "您已经参与过抽奖，每个IP只能抽取一次！"
        
        if not self.numbers:
            return None, "很抱歉，所有数字已被抽完！"
        
        # 从号码库中抽取一个号码
        while True:
            if not self.numbers:  # 再次检查，以防并发情况
                return None, "很抱歉，所有数字已被抽完！"
            
            number = self.numbers.pop()  # 取出最后一个号码
            
            # 检查号码是否已被使用
            if number not in self.used_numbers:
                self.used_numbers.add(number)  # 添加到已使用集合
                break
            # 如果号码已被使用，继续循环尝试下一个
        
        self.drawn_numbers[ip] = {
            'number': number,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return number, "恭喜！"

    def get_drawn_numbers_list(self):
        """获取所有已抽取的号码列表"""
        return [info['number'] for info in self.drawn_numbers.values()]

    def draw_winner(self):
        """从已抽取的号码中随机选择一个作为中奖号码"""
        drawn_numbers = self.get_drawn_numbers_list()
        if not drawn_numbers:
            return None, "还没有人参与抽奖！"
        winner = random.choice(drawn_numbers)
        return winner, "恭喜！"

# 创建抽奖状态实例
lottery = LotteryState()

@app.route('/')
def index():
    # 获取用户IP
    user_ip = request.remote_addr
    # 获取该IP已抽取的号码
    drawn_number = {'number': lottery.drawn_numbers.get(user_ip)} if user_ip in lottery.drawn_numbers else None
    
    return render_template('index.html', 
                         is_active=lottery.is_active,
                         drawn_number=drawn_number)

@app.route('/draw', methods=['POST'])
def draw():
    user_ip = request.remote_addr
    number, message = lottery.draw(user_ip)
    
    if number is None:
        return jsonify({
            'success': False,
            'message': message
        })
    
    return jsonify({
        'success': True,
        'message': f'恭喜！您抽到的数字是：{number}',
        'number': number
    })

@app.route('/admin')
def admin():
    # 将抽奖记录转换为列表并按时间排序
    drawn_list = [
        {
            'number': info['number'],
            'drawn_by_ip': ip,
            'drawn_at': info['time']
        }
        for ip, info in lottery.drawn_numbers.items()
    ]
    # 按时间倒序排序
    drawn_list.sort(key=lambda x: x['drawn_at'], reverse=True)
    
    return render_template('admin.html', 
                         drawn_numbers=drawn_list,
                         total_numbers=len(lottery.numbers) + len(lottery.drawn_numbers),
                         remaining_count=len(lottery.numbers),
                         is_active=lottery.is_active)

@app.route('/toggle_lottery', methods=['POST'])
def toggle_lottery():
    lottery.is_active = not lottery.is_active
    status = "开启" if lottery.is_active else "关闭"
    return redirect(url_for('admin'))

@app.route('/reset_lottery', methods=['POST'])
def reset_lottery():
    lottery.is_active = False
    lottery.reset()
    return redirect(url_for('admin'))

@app.route('/lucky')
def lucky_draw():
    drawn_count = len(lottery.drawn_numbers)
    return render_template('lucky.html', 
                         is_active=lottery.is_active,
                         drawn_count=drawn_count)

@app.route('/draw_winner', methods=['POST'])
def draw_winner():
    if not lottery.is_active:
        return jsonify({
            'success': False,
            'message': '抽奖活动尚未开始或已经结束！'
        })
    
    number, message = lottery.draw_winner()
    if number is None:
        return jsonify({
            'success': False,
            'message': message
        })
    
    return jsonify({
        'success': True,
        'message': f'恭喜！中奖号码是：{number}',
        'number': number
    })

@app.route('/get_participant_count')
def get_participant_count():
    return jsonify({
        'count': len(lottery.drawn_numbers),
        'is_active': lottery.is_active
    })

if __name__ == '__main__':
    app.run(debug=True) 