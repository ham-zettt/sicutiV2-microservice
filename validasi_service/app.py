from flask import Flask, jsonify, request, render_template
from models import db, PengajuanCuti

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/sicuti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def get_leave_requests():
    if request.method == 'POST':
        data = request.get_json()

        pengajuan_id = data.get("id")
        action = data.get("action")
        pengajuan = PengajuanCuti.query.get_or_404(pengajuan_id)
        
        if action == 'approve':
            pengajuan.status = 'Disetujui'
            message = "Leave request approved!"
        elif action == 'reject':
            pengajuan.status = 'Ditolak'
            message = "Leave request rejected!"
        else:
            message = "Invalid action"

        db.session.commit()
        return jsonify({"message": message})

    data_cuti = PengajuanCuti.query.all()
    return render_template('home.html', data=data_cuti)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')