from flask import Blueprint, request, jsonify
from app.models import Song
from app.extensions import db
from app.utils.decorators import token_required

songs_bp = Blueprint('songs', __name__, url_prefix='/songs')
@songs_bp.route('/get', methods=['GET'])
def get_songs():
    """获取歌单列表"""
    songs = Song.query.order_by(Song.id.desc()).all()
    return jsonify([song.to_dict() for song in songs])

@songs_bp.route('/add', methods=['POST'])
@token_required
def create_song():
    """创建新歌曲"""
    data = request.get_json()

    title = data.get('title').strip()
    artist = data.get('artist').strip()
    url = data.get('url').strip()
    cover = data.get('cover').strip()

    new_song = Song(
        title=title,
        artist=artist,
        url=url,
        cover=cover
    )
    
    db.session.add(new_song)
    db.session.commit()

    return jsonify(new_song.to_dict()), 201

@songs_bp.route('/delete', methods=['POST'])
@token_required
def delete_song():
    """删除歌曲"""
    data = request.get_json()
    song_id = data.get('id')
    song = Song.query.get_or_404(song_id)
    if not song:
        return jsonify({"error": "歌曲不存在"}), 404
    db.session.delete(song)
    db.session.commit()

    return jsonify({"message": "歌曲已删除"})

@songs_bp.route('/update', methods=['POST'])
@token_required
def update_song():
    """更新歌曲"""
    #获取请求数据
    data = request.get_json()
    #提取歌曲ID
    song_id = data.get('id')
    #查询歌曲并更新数据
    song = Song.query.get_or_404(song_id)
    if not song:
        return jsonify({"error": "歌曲不存在"}), 404

    song.title = data.get('title', song.title).strip()
    song.artist = data.get('artist', song.artist).strip()
    song.url = data.get('url', song.url).strip()
    song.cover = data.get('cover', song.cover).strip()

    db.session.commit()

    return jsonify(song.to_dict())

@songs_bp.route('/addlist', methods=['POST'])
@token_required
def add_song_list():
    """批量添加歌曲"""
    songs_data = request.get_json()
    new_songs = []
    for song_data in songs_data:
        title = song_data.get('title').strip()
        artist = song_data.get('artist').strip()
        url = song_data.get('url').strip()
        cover = song_data.get('cover').strip()

        new_song = Song(
            title=title,
            artist=artist,
            url=url,
            cover=cover
        )
        new_songs.append(new_song)

    if new_songs:
        db.session.add_all(new_songs)
        db.session.commit()

    return jsonify({"message": f"成功添加 {len(new_songs)} 首歌曲"}), 201