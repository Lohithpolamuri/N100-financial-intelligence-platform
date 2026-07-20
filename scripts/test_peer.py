print("=" * 50)
print("STARTING PEER ANALYTICS TEST")
print("=" * 50)

from src.analytics.peer import PeerAnalytics

peer = PeerAnalytics()

peer.save_to_database()
peer = PeerAnalytics()

print(peer.master_df.columns.tolist())
print(peer.get_peer_group("HDFCBANK"))
print(peer.get_peer_group("XYZ"))