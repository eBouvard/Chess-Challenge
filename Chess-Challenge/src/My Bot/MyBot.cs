using System.ComponentModel;
using System.IO.Compression;
using System.Reflection.Metadata;
using ChessChallenge.API;

// --- ONLY FOR TRAINING, TO DELETE LATER

using System;
using System.IO;
using System.Linq;

// ONLY FOR TRAINING, TO DELETE LATER ---

public class MyBot : IChessBot
{

    static ulong magicNumberFen = 1;
    static ulong[] magicNumbersW = { 0, 1, 3, 3, 5, 9, 0 };
    static ulong[] magicNumbersB = { 0, 1, 3, 3, 5, 9, 0 };
    public MyBot()
    {
        LoadMagicNumbersFromFile("magicNumbers.txt");
    }

    private void LoadMagicNumbersFromFile(string path)
    {
        try
        {
            var lines = File.ReadAllLines(path);
            foreach (var line in lines)
            {
                var parts = line.Split(':');
                if (parts.Length != 2) continue;  // skip invalid lines

                var key = parts[0].Trim();
                var value = parts[1].Trim();

                switch (key)
                {
                    case "MagicNumberFen":
                        magicNumberFen = ulong.Parse(value);
                        break;
                    case "MagicNumbersW":
                        magicNumbersW = value.Split(',').Select(ulong.Parse).ToArray();
                        break;
                    case "MagicNumbersB":
                        magicNumbersB = value.Split(',').Select(ulong.Parse).ToArray();
                        break;
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error reading magic numbers from file: " + ex.Message);
        }
    }

    static ulong SimpleHash(string input)
    {
        ulong hash = 0;
        foreach (char c in input)
        {
            hash = (hash * 31) + c;
        }
        return hash;
    }

    private ulong EvalBitBoards(Board board, bool isW)
    {
        var fenStringFactor = SimpleHash(board.GetFenString()) * magicNumberFen;
        int whiteFactor = isW ? 1 : -1;
        ulong score = 0;
        for (int i = 1; i < 6; i++)
        {
            ulong bitW = board.GetPieceBitboard((PieceType)i, true);
            ulong bitB = board.GetPieceBitboard((PieceType)i, false);

            score += (ulong)whiteFactor * (magicNumbersW[i] * bitW - magicNumbersB[i] * bitB);
        }
        return score * fenStringFactor;
    }

    public Move Think(Board board, Timer timer)
    {
        bool isW = board.IsWhiteToMove;
        Move[] moves = board.GetLegalMoves();
        (ulong score, int index) bestMove = (ulong.MinValue, -1);
        for (int i = 0; i < moves.Length; i++)
        {
            board.MakeMove(moves[i]);

            ulong score = EvalBitBoards(board, isW);
            if (score > bestMove.score)
            {
                bestMove = (score, i);
            }

            board.UndoMove(moves[i]);
        }
        return moves[bestMove.index];
    }
}