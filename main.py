import argparse
from audio_utils import load_audio, save_audio
from binary_utils import text_to_bits, bits_to_text
from echo_hiding import embed_message
from echo_decoding import extract_message
from eval_metrics import bit_error_rate, normalized_correlation


#
# EMBED
#
def embed_watermark(input_audio, msg_file, out_audio, d0=150, d1=200, alpha=0.5, frame_size=8192):
    print("Loading audio file")
    signal, sample_rate = load_audio(input_audio)

    print("Reading message file.")
    with open(msg_file, 'r') as f:
        msg = f.read()


    print("Embedding message into the audio file.")
    stego_signal = embed_message(signal, msg, d0, d1, alpha, frame_size)

    print("Saving watermarked audio file.")
    save_audio(out_audio, stego_signal, sample_rate)

    print("Watermarked audio saved to: ", out_audio)


#
# EXTRACT
#
def extract_watermark(input_audio, frame_size=8192, d0=150, d1=200):
    print("Loading the watermarked audio file.")
    signal, sample_rate = load_audio(input_audio)

    print("Extracting the watermark from the audio file.")
    extracted = extract_message(signal, frame_size, d0, d1)

    print("Extracted message: ")
    print(extracted)
    return extracted


#
# EVALUATE
#
def evaluate_watermark(og_msg_file, extracted_wm):
    print("Reading original message.")
    with open(og_msg_file, 'r') as f:
        og_msg = f.read()

    print("Calculating evaluation metrics.")
    og_bits = text_to_bits(og_msg)
    extracted_bits = text_to_bits(extracted_wm)

    ber = bit_error_rate(og_bits, extracted_bits)
    nc = normalized_correlation(og_bits, extracted_bits)

    print(f"Bit Error Rate: {ber:.2f}%")
    print(f"Normalized Correlation: {nc:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Echo Hiding Audio Watermarking Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    embed_parser = subparsers.add_parser("embed", help="Embed a message into an audio file")
    embed_parser.add_argument("input_audio", help="Path to the input audio file")
    embed_parser.add_argument("message_file", help="Path to the text message file")
    embed_parser.add_argument("output_audio", help="Path to save the output watermarked audio file")
    embed_parser.add_argument("--d0", type=int, default=150, help="Echo delay for bit 0")
    embed_parser.add_argument("--d1", type=int, default=200, help="Echo delay for bit 1")
    embed_parser.add_argument("--alpha", type=float, default=0.5, help="Echo amplitude")
    embed_parser.add_argument("--frame_size", type=int, default=8192, help="Frame size for embedding")

    extract_parser = subparsers.add_parser("extract", help="Extract a message from a watermarked audio file")
    extract_parser.add_argument("input_audio", help="Path to the watermarked audio file")
    extract_parser.add_argument("--frame_size", type=int, default=8192, help="Frame size for extraction")
    extract_parser.add_argument("--d0", type=int, default=150, help="Echo delay for bit 0")
    extract_parser.add_argument("--d1", type=int, default=200, help="Echo delay for bit 1")

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate watermarking performance")
    evaluate_parser.add_argument("original_message_file", help="Path to the original text message file")
    evaluate_parser.add_argument("extracted_message_file", help="Path to the extracted message file")

    args = parser.parse_args()

    if args.command == "embed":
        embed_watermark(args.input_audio, args.message_file, args.output_audio, args.d0, args.d1, args.alpha, args.frame_size)
    elif args.command == "extract":
        extracted_message = extract_watermark(args.input_audio, args.frame_size, args.d0, args.d1)
        print("Extracted message:")
        print(extracted_message)
    elif args.command == "evaluate":
        evaluate_watermark(args.original_message_file, args.extracted_message_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

