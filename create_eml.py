import io
import argparse
from sys import exit
from loguru import logger
from html2eml import html2eml
from email.policy import default
from email.parser import BytesParser


def append_attachment(eml_content, attachment, attachment_name):
    msg = BytesParser(policy=default).parse(eml_content)
    msg.add_attachment(attachment, 'attachment', attachment_name.split(".")[1], filename=attachment_name)
    return msg.as_bytes()

def main(args):
    html = open(args.html, "r").read()
    html = html.replace("\\r", "\r")
    html = html.replace("\\n", "\n")

    msg = html2eml.from_html(html, to=args.to, from_=args.from_, subject=args.subject)

    if args.a:
        attachment = open(args.a, "rb").read()
        attachment_name = args.an
        out = append_attachment(io.BytesIO(msg.as_bytes()), attachment, attachment_name)
    else:
        out = msg.as_bytes()

    open(args.o, "wb").write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-to", help="Email To field", required=True, type=str)
    parser.add_argument("-from_", help="Email From field", required=True, type=str)
    parser.add_argument("-s", "--subject", help="Email Subject field", required=True, type=str)
    parser.add_argument("-html", help="File containing the HTML body of the email", required=False, type=str)
    parser.add_argument("-a", help="Attachment file", required=False, type=str)
    parser.add_argument("-an", help="Attachment name", required=False, type=str)
    parser.add_argument("-o", help="Output EML file name", required=True, type=str)

    args = parser.parse_args()

    if (args.a and not args.an) or (args.an and not args.a):
        logger.info("you need to specify always both the attachment file (-a) and the attachment name (-an) that will appear on the EML file")

    main(args)

