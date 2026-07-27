from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id, languages=['en', 'id'])
        # The fetch method returns a FetchedTranscript object, 
        # and the actual transcript snippets are in the .snippets attribute
        return " ".join([snippet.text for snippet in transcript_obj.snippets])
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_transcript(sys.argv[1]))
    else:
        print("Please provide a video ID")
