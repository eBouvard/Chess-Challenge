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

    long magicNumberFen = 1;
    long[] magicNumbersWTop = { 0, 1, 3, 3, 5, 9, 0 };
    long[] magicNumbersBTop = { 0, 1, 3, 3, 5, 9, 0 };
    long[] magicNumbersWBot = { 0, 1, 3, 3, 5, 9, 0 };
    long[] magicNumbersBBot = { 0, 1, 3, 3, 5, 9, 0 };


    // --- ONLY FOR TRAINING, TO DELETE LATER
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
                        magicNumberFen = long.Parse(value);
                        break;
                    case "MagicNumbersWTop":
                        magicNumbersWTop = value.Split(',').Select(long.Parse).ToArray();
                        break;
                    case "MagicNumbersBTop":
                        magicNumbersBTop = value.Split(',').Select(long.Parse).ToArray();
                        break;
                    case "MagicNumbersWBot":
                        magicNumbersWBot = value.Split(',').Select(long.Parse).ToArray();
                        break;
                    case "MagicNumbersBBot":
                        magicNumbersBBot = value.Split(',').Select(long.Parse).ToArray();
                        break;
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error reading magic numbers from file: " + ex.Message);
        }
    }

    // ONLY FOR TRAINING, TO DELETE LATER ---

    static long SimpleHash(string input)
    {
        long hash = 0;
        foreach (char c in input)
        {
            hash = (hash * 31) + c;
        }
        return hash;
    }

    private long EvalBitBoards(Board board, bool isW)
    {
        var fenStringFactor = SimpleHash(board.GetFenString()) * magicNumberFen;
        int whiteFactor = isW ? 1 : -1;
        long score = 0;
        for (int i = 1; i < 6; i++)
        {
            uint bitW_T = (uint)(board.GetPieceBitboard((PieceType)i, true) >> 32);
            uint bitB_T = (uint)(board.GetPieceBitboard((PieceType)i, false) >> 32);
            uint bitW_B = (uint)board.GetPieceBitboard((PieceType)i, true);
            uint bitB_B = (uint)board.GetPieceBitboard((PieceType)i, false);

            score += whiteFactor * (
                magicNumbersWTop[i] * bitW_T
                + magicNumbersWBot[i] * bitW_B
                - magicNumbersBTop[i] * bitB_T
                - magicNumbersBBot[i] * bitB_B
                );
        }
        return score * fenStringFactor;
    }

    public Move Think(Board board, Timer timer)
    {
        bool isW = board.IsWhiteToMove;
        Move[] moves = board.GetLegalMoves();
        (long score, int index) bestMove = (long.MinValue, -1);
        for (int i = 0; i < moves.Length; i++)
        {
            board.MakeMove(moves[i]);

            long score = EvalBitBoards(board, isW);
            if (score > bestMove.score)
            {
                bestMove = (score, i);
            }

            board.UndoMove(moves[i]);
        }
        if (bestMove.index == -1) return moves[0];
        return moves[bestMove.index];
    }
}