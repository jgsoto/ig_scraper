def calculate_engagement(posts, followers=None):
    if not posts:
        return {}

    total_likes = sum(p["likes"] for p in posts)
    total_comments = sum(p["comments"] for p in posts)

    total_engagement = total_likes + total_comments

    engagement_posts = [
        {
            "url": p["url"],
            "likes": p["likes"],
            "comments": p["comments"],
            "engagement": p["likes"] + p["comments"]
        }
        for p in posts
    ]

    engagement_posts_sorted = sorted(
        engagement_posts,
        key=lambda x: x["engagement"],
        reverse=True
    )

    avg_engagement = total_engagement / len(posts)

    engagement_rate_followers = None
    if followers and followers > 0:
        engagement_rate_followers = total_engagement / followers

    values = [p["likes"] + p["comments"] for p in posts]
    variance = sum((x - avg_engagement) ** 2 for x in values) / len(values)

    return {
        "total_posts": len(posts),
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_engagement": total_engagement,
        "avg_engagement": avg_engagement,
        "engagement_rate_followers": engagement_rate_followers,
        "top_post": engagement_posts_sorted[0],
        "top_5_posts": engagement_posts_sorted[:5],
        "consistency_variance": variance
    }