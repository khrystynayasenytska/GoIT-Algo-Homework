class Comment:
    def __init__(self, text, author):
        self.text = text
        self.author = author
        self.replies = []          # list of child comments
        self.is_deleted = False    # deletion flag

    def add_reply(self, reply_comment):
        """Adds a reply to the current comment."""
        self.replies.append(reply_comment)

    def remove_reply(self):
        """
        Logical deletion of comment:
        changes text to standard message and sets is_deleted = True.
        """
        self.text = "This comment has been deleted."
        self.is_deleted = True

    def display(self, indent=0):
        """
        Recursively displays comment and all its replies with indentation.
        """
        prefix = " " * indent
        if self.is_deleted:
            # show only the text of deleted comment
            print(f"{prefix}{self.text}")
        else:
            print(f"{prefix}{self.author}: {self.text}")

        # recursively display replies, increasing indentation
        for reply in self.replies:
            reply.display(indent + 4)


# Example of usage
if __name__ == "__main__":
    root_comment = Comment("What a wonderful book!", "Bodya")
    reply1 = Comment("The book is a total disappointment :(", "Andrii")
    reply2 = Comment("What's wonderful about it?", "Marina")

    root_comment.add_reply(reply1)
    root_comment.add_reply(reply2)

    reply1_1 = Comment("Not a book, just wasted paper for nothing...", "Sergii")
    reply1.add_reply(reply1_1)

    # logically "delete" Andrii's comment
    reply1.remove_reply()

    root_comment.display()
